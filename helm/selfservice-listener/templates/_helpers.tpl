{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}
{{- /*
These template definitions relate to the use of this Helm chart as a sub-chart of the Nubus Umbrella Chart.
Templates defined in other Helm sub-charts are imported to be used to configure this chart.
If the value .Values.global.nubusDeployment equates to true, the defined templates are imported.
*/}}
{{- define "selfservice-listener.provisioningApi.connection.baseUrl" -}}
{{- if .Values.provisioningApi.connection.baseUrl -}}
{{- tpl .Values.provisioningApi.connection.baseUrl . -}}
{{- else if .Values.global.nubusDeployment -}}
{{- $protocol := "http" -}}
{{- $host := include "nubusTemplates.provisioningApi.connection.host" . -}}
{{- printf "%s://%s" $protocol $host -}}
{{- else -}}
{{- required ".Values.provisioningApi.connection.baseUrl must be defined." .Values.provisioningApi.connection.baseUrl -}}
{{- end -}}
{{- end -}}

{{- /*
These template definitions are only used in this chart and do not relate to templates defined elsewhere.
*/}}
{{- define "selfservice-listener.umc.connection.baseUrl" -}}
{{- if .Values.umc.connection.baseUrl -}}
{{- tpl .Values.umc.connection.baseUrl . -}}
{{- else if .Values.global.nubusDeployment -}}
{{- $protocol := "http" -}}
{{- printf "%s://%s-umc-server" $protocol .Release.Name -}}
{{- else -}}
{{- required ".Values.umc.connection.baseUrl must be defined." .Values.umc.connection.baseUrl -}}
{{- end -}}
{{- end -}}

{{- define "selfservice-listener.provisioningApi.auth.username" -}}
{{- if .Values.provisioningApi.auth.username -}}
{{- .Values.provisioningApi.auth.username -}}
{{- else -}}
{{- required ".Values.provisioningApi.auth.username must be defined." .Values.provisioningApi.auth.username -}}
{{- end -}}
{{- end -}}

{{- define "selfservice-listener.umc.auth.username" -}}
{{- if .Values.umc.auth.username -}}
{{- .Values.umc.auth.username -}}
{{- else -}}
{{- required ".Values.umc.auth.username must be defined." .Values.umc.auth.username -}}
{{- end -}}
{{- end -}}

{{- define "selfservice-listener.umc.auth.credentialSecret.name" -}}
{{- if .Values.umc.auth.credentialSecret.name -}}
{{- .Values.umc.auth.credentialSecret.name -}}
{{- else if .Values.umc.auth.password -}}
{{ printf "%s-umc-credentials" (include "common.names.fullname" .) }}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-selfservice-listener-credentials" .Release.Name -}}
{{- else -}}
{{ required ".Values.umc.auth.password must be defined." .Values.umc.auth.password}}
{{- end -}}
{{- end -}}

{{- define "selfservice-listener.umc.auth.password" -}}
{{- if .Values.umc.auth.credentialSecret.name -}}
valueFrom:
  secretKeyRef:
    name: {{ .Values.umc.auth.credentialSecret.name | quote }}
    key: {{ .Values.umc.auth.credentialSecret.key | quote }}
{{- else if .Values.global.nubusDeployment -}}
valueFrom:
  secretKeyRef:
    name: {{ include "selfservice-listener.umc.auth.credentialSecret.name" . | quote }}
    key: {{ .Values.umc.auth.credentialSecret.key | quote }}
{{- else -}}
value: {{ required ".Values.umc.auth.password is required." .Values.umc.auth.password | quote }}
{{- end -}}
{{- end -}}

{{- define "selfservice-listener.provisioningApi.auth.credentialSecret.name" -}}
{{- if .Values.provisioningApi.auth.credentialSecret.name -}}
{{- .Values.provisioningApi.auth.credentialSecret.name -}}
{{- else if .Values.provisioningApi.auth.password -}}
{{ printf "%s-api-credentials" (include "common.names.fullname" .) }}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-selfservice-listener-credentials" .Release.Name -}}
{{- else -}}
{{ required ".Values.provisioningApi.auth.password must be defined." .Values.provisioningApi.auth.password}}
{{- end -}}
{{- end -}}

{{- define "selfservice-listener.provisioningApi.auth.password" -}}
{{- if .Values.provisioningApi.auth.credentialSecret.name -}}
valueFrom:
  secretKeyRef:
    name: {{ .Values.provisioningApi.auth.credentialSecret.name | quote }}
    key: {{ .Values.provisioningApi.auth.credentialSecret.key | quote }}
{{- else if .Values.global.nubusDeployment -}}
valueFrom:
  secretKeyRef:
    name: {{ include "selfservice-listener.provisioningApi.auth.credentialSecret.name" . | quote }}
    key: {{ .Values.provisioningApi.auth.credentialSecret.key | quote }}
{{- else -}}
value: {{ required ".Values.provisioningApi.auth.password is required." .Values.umc.auth.password | quote }}
{{- end -}}
{{- end -}}
