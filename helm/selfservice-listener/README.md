# selfservice-listener

The selfservice listener for handling user invites

- **Version**: 0.1.0
- **Type**: application
- **AppVersion**: 0.0.1
-

## Introduction

This chart does install a the selfservice listener container.

It is intended to listen for newly created users, starting the flow to send the
user an email to set their password.

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/common-helm/helm | common | ^0.2.0 |

## Values

<table>
	<thead>
		<th>Key</th>
		<th>Type</th>
		<th>Default</th>
		<th>Description</th>
	</thead>
	<tbody>
		<tr>
			<td>affinity</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>containerSecurityContext.allowPrivilegeEscalation</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td>Enable container privileged escalation.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.capabilities</td>
			<td>object</td>
			<td><pre lang="json">
{
  "drop": [
    "ALL"
  ]
}
</pre>
</td>
			<td>Security capabilities for container.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Enable security context.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.readOnlyRootFilesystem</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Mounts the container's root filesystem as read-only.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.runAsGroup</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td>Process group id.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.runAsNonRoot</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Run container as a user.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.runAsUser</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td>Process user id.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.seccompProfile.type</td>
			<td>string</td>
			<td><pre lang="json">
"RuntimeDefault"
</pre>
</td>
			<td>Disallow custom Seccomp profile by setting it to RuntimeDefault.</td>
		</tr>
		<tr>
			<td>environment</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>extraEnvVars</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Optionally specify a secret to create (primarily intended to be used in development environments to provide custom certificates)</td>
		</tr>
		<tr>
			<td>extraSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Optionally specify a secret to create (primarily intended to be used in development environments to provide custom certificates)</td>
		</tr>
		<tr>
			<td>fullnameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.imagePullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
"IfNotPresent"
</pre>
</td>
			<td>Define an ImagePullPolicy.  Ref.: https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy  "IfNotPresent" => The image is pulled only if it is not already present locally. "Always" => Every time the kubelet launches a container, the kubelet queries the container image registry to             resolve the name to an image digest. If the kubelet has a container image with that exact digest cached             locally, the kubelet uses its cached image; otherwise, the kubelet pulls the image with the resolved             digest, and uses that image to launch the container. "Never" => The kubelet does not try fetching the image. If the image is somehow already present locally, the            kubelet attempts to start the container; otherwise, startup fails.</td>
		</tr>
		<tr>
			<td>global.imagePullSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Credentials to fetch images from private registry Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" </td>
		</tr>
		<tr>
			<td>global.imageRegistry</td>
			<td>string</td>
			<td><pre lang="json">
"artifacts.software-univention.de"
</pre>
</td>
			<td>Container registry address.</td>
		</tr>
		<tr>
			<td>global.nubusDeployment</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td>Indicates wether this chart is part of a Nubus deployment.</td>
		</tr>
		<tr>
			<td>image.imagePullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
"IfNotPresent"
</pre>
</td>
			<td>The pull policy of the container image.  This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Container registry address. This setting has higher precedence than global.registry.</td>
		</tr>
		<tr>
			<td>image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus-dev/images/selfservice-invitation"
</pre>
</td>
			<td>The path to the container image.</td>
		</tr>
		<tr>
			<td>image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td>The tag of the container image. (This is replaced with an appropriate value during the build process of the Helm chart.)</td>
		</tr>
		<tr>
			<td>nameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>nodeSelector</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>podAnnotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>podSecurityContext</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>provisioningApi.auth</td>
			<td>object</td>
			<td><pre lang="json">
{
  "credentialSecret": {
    "key": "PROVISIONING_API_PASSWORD",
    "name": ""
  },
  "password": "",
  "username": "selfservice"
}
</pre>
</td>
			<td>Authentication parameters</td>
		</tr>
		<tr>
			<td>provisioningApi.auth.credentialSecret</td>
			<td>object</td>
			<td><pre lang="json">
{
  "key": "PROVISIONING_API_PASSWORD",
  "name": ""
}
</pre>
</td>
			<td>The name of the secret containing the password.</td>
		</tr>
		<tr>
			<td>provisioningApi.auth.credentialSecret.key</td>
			<td>string</td>
			<td><pre lang="json">
"PROVISIONING_API_PASSWORD"
</pre>
</td>
			<td>The key where the password can be found.</td>
		</tr>
		<tr>
			<td>provisioningApi.auth.credentialSecret.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The name of the secret.</td>
		</tr>
		<tr>
			<td>provisioningApi.auth.password</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The password to authenticate with.</td>
		</tr>
		<tr>
			<td>provisioningApi.auth.username</td>
			<td>string</td>
			<td><pre lang="json">
"selfservice"
</pre>
</td>
			<td>The username to authenticate with.</td>
		</tr>
		<tr>
			<td>provisioningApi.config.maxAcknowledgementRetries</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td>The maximum number of retries for acknowledging a message</td>
		</tr>
		<tr>
			<td>provisioningApi.connection</td>
			<td>object</td>
			<td><pre lang="json">
{
  "baseUrl": ""
}
</pre>
</td>
			<td>Connection parameters</td>
		</tr>
		<tr>
			<td>provisioningApi.connection.baseUrl</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The base URL the provisioning API is reachable at. (e.g. "https://provisioning-api")</td>
		</tr>
		<tr>
			<td>replicaCount</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>securityContext</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.config.logLevel</td>
			<td>string</td>
			<td><pre lang="json">
"INFO"
</pre>
</td>
			<td>Log level for the selfservice listener. valid values are: ERROR WARNING, INFO, DEBUG</td>
		</tr>
		<tr>
			<td>selfserviceListener.config.maxUmcRequestRetries</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.automountServiceAccountToken</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.create</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.labels</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom labels for the ServiceAccount.</td>
		</tr>
		<tr>
			<td>serviceAccount.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>tolerations</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>umc.auth</td>
			<td>object</td>
			<td><pre lang="json">
{
  "credentialSecret": {
    "key": "UMC_ADMIN_PASSWORD",
    "name": ""
  },
  "password": "",
  "username": "cn=admin"
}
</pre>
</td>
			<td>Authentication parameters</td>
		</tr>
		<tr>
			<td>umc.auth.credentialSecret</td>
			<td>object</td>
			<td><pre lang="json">
{
  "key": "UMC_ADMIN_PASSWORD",
  "name": ""
}
</pre>
</td>
			<td>The name of the secret containing the password.</td>
		</tr>
		<tr>
			<td>umc.auth.credentialSecret.key</td>
			<td>string</td>
			<td><pre lang="json">
"UMC_ADMIN_PASSWORD"
</pre>
</td>
			<td>The key where the password can be found.</td>
		</tr>
		<tr>
			<td>umc.auth.credentialSecret.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The name of the secret.</td>
		</tr>
		<tr>
			<td>umc.auth.password</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The password to authenticate with.</td>
		</tr>
		<tr>
			<td>umc.auth.username</td>
			<td>string</td>
			<td><pre lang="json">
"cn=admin"
</pre>
</td>
			<td>The username to authenticate with.</td>
		</tr>
		<tr>
			<td>umc.connection</td>
			<td>object</td>
			<td><pre lang="json">
{
  "baseUrl": ""
}
</pre>
</td>
			<td>Connection parameters</td>
		</tr>
		<tr>
			<td>umc.connection.baseUrl</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The base URL the UMC is reachable at. (e.g. "https://umc-server")</td>
		</tr>
	</tbody>
</table>

