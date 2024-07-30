{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}
{{- /*
These template definitions relate to the use of this Helm chart as a sub-chart of the Nubus Umbrella Chart.
Templates defined in other Helm sub-charts are imported to be used to configure this chart.
If the value .Values.global.nubusDeployment equates to true, the defined templates are imported.
*/}}
{{- define "selfserviceLister.umcServerUrl" -}}
{{- if .Values.selfserviceListener.umcServerUrl -}}
{{- .Values.selfserviceListener.umcServerUrl -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "http://%s-umc-server" .Release.Name -}}
{{- else -}}
http://umc-server
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.ldapBaseDn" -}}
{{- if .Values.selfserviceListener.ldapBaseDn -}}
{{- .Values.selfserviceListener.ldapBaseDn -}}
{{- else if .Values.global.nubusDeployment -}}
{{- include "nubusTemplates.ldapServer.ldap.baseDn" . -}}
{{- else -}}
dc=univention-organization,dc=intranet
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.ldapAdminDn" -}}
{{- if .Values.selfserviceListener.ldapHostDn -}}
{{- .Values.selfserviceListener.ldapHostDn -}}
{{- else if .Values.global.nubusDeployment -}}
{{- include "nubusTemplates.ldapServer.ldap.adminDn" . -}}
{{- else -}}
cn=admin,dc=univention-organization,dc=intranet
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.ldap.connection.host" -}}
{{- if .Values.selfserviceListener.ldapHost -}}
{{- tpl .Values.selfserviceListener.ldapHost . -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-ldap-server-primary" .Release.Name -}}
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.ldap.connection.port" -}}
{{- if .Values.selfserviceListener.ldapPort -}}
{{- .Values.selfserviceListener.ldapPort -}}
{{- else if .Values.global.nubusDeployment -}}
{{- include "nubusTemplates.ldapServer.ldap.connection.port" . -}}
{{- end -}}
{{- end -}}


{{- define "selfserviceListener.ldapDomainName" -}}
{{- if .Values.selfserviceListener.domainName -}}
{{- .Values.selfserviceListener.domainName -}}
{{- else if .Values.global.nubusDeployment -}}
{{- include "nubusTemplates.ldapServer.ldap.domainName" . -}}
{{- else -}}
univention-organization.intranet
{{- end -}}
{{- end -}}



{{- /*
These template definitions are only used in this chart and do not relate to templates defined elsewhere.
*/}}


{{- define "selfserviceListener.umcAdminPasswordSecret.name" -}}
{{- if .Values.selfserviceListener.umcAdminPasswordSecret.name -}}
{{- .Values.selfserviceListener.umcAdminPasswordSecret.name -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-self-service-ldap-credentials" .Release.Name -}}
{{- else -}}
{{- required ".Values.selfserviceListener.umcAdminPasswordSecret.name is required" .Values.selfserviceListener.umcAdminPasswordSecret.name -}}
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.umcAdminPasswordSecret.key" -}}
{{- if .Values.selfserviceListener.umcAdminPasswordSecret.key -}}
{{- .Values.selfserviceListener.umcAdminPasswordSecret.key -}}
{{- else if .Values.global.nubusDeployment -}}
password
{{- else -}}
{{- required ".Values.selfserviceListener.umcAdminPasswordSecret.key is required" .Values.selfserviceListener.umcAdminPasswordSecret.key -}}
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.tlsSecretTemplate" -}}
{{- if (index . 2).Release.Name -}}
{{- $secretName := printf "%s-%s-tls" (index . 2).Release.Name (index . 0) -}}
{{- if (index . 1).name -}}
{{- (index . 1).name -}}
{{- else if (index . 2).Values.global.nubusDeployment -}}
{{- $secretName -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.secretTemplate" -}}
{{- if (index . 2).Release.Name -}}
{{- $secretName := printf "%s-%s-credentials" (index . 2).Release.Name (index . 0) -}}
{{- if (index . 1).name -}}
{{- (index . 1).name -}}
{{- else if (index . 2).Values.global.nubusDeployment -}}
{{- $secretName -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.ldap.credentialSecret.name" -}}
{{- include "selfserviceListener.secretTemplate" (list "selfservice-listener-ldap" .Values.ldap.credentialSecret .) -}}
{{- end -}}

{{- define "selfserviceListener.ldap.tlsSecret.name" -}}
{{- include "selfserviceListener.tlsSecretTemplate" (list "selfservice-listener-ldap" .Values.ldap.tlsSecret .) -}}
{{- end -}}


{{- define "selfserviceListener.notifierServer" -}}
{{- if .Values.selfserviceListener.notifierServer -}}
{{- .Values.selfserviceListener.notifierServer -}}
{{- else -}}
{{- printf "%s-ldap-notifier" .Release.Name -}}
{{- end -}}
{{- end -}}

{{- define "selfserviceListener.secretVolumeMounts" -}}
{{- $secretMountPath := .Values.selfserviceListener.secretMountPath -}}
{{- $tlsSecretName := include "selfserviceListener.ldap.tlsSecret.name" . -}}
{{- $credentialSecretName := include "selfserviceListener.ldap.credentialSecret.name" . -}}
{{- if $credentialSecretName }}
- name: {{ printf "%s-volume" $credentialSecretName | quote }}
  mountPath: "{{ $secretMountPath }}/ldap_secret"
  subPath: {{ .Values.ldap.credentialSecret.ldapPasswordKey | quote }}
  readOnly: true
{{- end }}
{{- if $tlsSecretName }}
- name: {{ printf "%s-volume" $tlsSecretName | quote }}
  mountPath: "{{ $secretMountPath }}/ca_cert"
  subPath: {{ .Values.ldap.tlsSecret.caCertKey | quote }}
  readOnly: true
- name: {{ printf "%s-volume" $tlsSecretName | quote }}
  mountPath: "{{ $secretMountPath }}/cert_pem"
  subPath: {{ .Values.ldap.tlsSecret.certificateKey | quote }}
  readOnly: true
- name: {{ printf "%s-volume" $tlsSecretName | quote }}
  mountPath: "{{ $secretMountPath }}/private_key"
  subPath: {{ .Values.ldap.tlsSecret.privateKeyKey | quote }}
  readOnly: true
{{- end }}
{{- end -}}
