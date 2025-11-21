# selfservice-consumer

The selfservice consumer for handling user invites

- **Version**: 0.11.3
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
| oci://artifacts.software-univention.de/nubus/charts | nubus-common | 0.28.0 |

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
			<td>containerSecurityContext.privileged</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
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
null
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
			<td>image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
""
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
			<td>initResources</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Custom resource requests and limits for the init containers.</td>
		</tr>
		<tr>
			<td>livenessProbe.exec.command[0]</td>
			<td>string</td>
			<td><pre lang="json">
"sh"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>livenessProbe.exec.command[1]</td>
			<td>string</td>
			<td><pre lang="json">
"-c"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>livenessProbe.exec.command[2]</td>
			<td>string</td>
			<td><pre lang="json">
"exit 0\n"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>livenessProbe.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
10
</pre>
</td>
			<td>Number of failed executions until container is terminated.</td>
		</tr>
		<tr>
			<td>livenessProbe.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td>Delay after container start until LivenessProbe is executed.</td>
		</tr>
		<tr>
			<td>livenessProbe.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td>Time between probe executions.</td>
		</tr>
		<tr>
			<td>livenessProbe.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td>Number of successful executions after failed ones until container is marked healthy.</td>
		</tr>
		<tr>
			<td>livenessProbe.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td>Timeout for command return.</td>
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
  "existingSecret": {
    "keyMapping": {
      "password": null
    },
    "name": null
  },
  "password": null,
  "username": "selfservice"
}
</pre>
</td>
			<td>Authentication parameters</td>
		</tr>
		<tr>
			<td>provisioningApi.auth.existingSecret</td>
			<td>object</td>
			<td><pre lang="json">
{
  "keyMapping": {
    "password": null
  },
  "name": null
}
</pre>
</td>
			<td>The name of the secret containing the password.</td>
		</tr>
		<tr>
			<td>provisioningApi.auth.password</td>
			<td>string</td>
			<td><pre lang="json">
null
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
  "url": ""
}
</pre>
</td>
			<td>Connection parameters</td>
		</tr>
		<tr>
			<td>provisioningApi.connection.url</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The base URL the provisioning API is reachable at. (e.g. "https://provisioning-api")</td>
		</tr>
		<tr>
			<td>readinessProbe.exec.command[0]</td>
			<td>string</td>
			<td><pre lang="json">
"sh"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>readinessProbe.exec.command[1]</td>
			<td>string</td>
			<td><pre lang="json">
"-c"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>readinessProbe.exec.command[2]</td>
			<td>string</td>
			<td><pre lang="json">
"exit 0\n"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>readinessProbe.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
10
</pre>
</td>
			<td>Number of failed executions until container is terminated.</td>
		</tr>
		<tr>
			<td>readinessProbe.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td>Delay after container start until ReadinessProbe is executed.</td>
		</tr>
		<tr>
			<td>readinessProbe.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td>Time between probe executions.</td>
		</tr>
		<tr>
			<td>readinessProbe.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td>Number of successful executions after failed ones until container is marked healthy.</td>
		</tr>
		<tr>
			<td>readinessProbe.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td>Timeout for command return.</td>
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
			<td>resources</td>
			<td>object</td>
			<td><pre lang="json">
{}
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
			<td>umc.connection</td>
			<td>object</td>
			<td><pre lang="json">
{
  "url": ""
}
</pre>
</td>
			<td>Connection parameters</td>
		</tr>
		<tr>
			<td>umc.connection.url</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The base URL the UMC is reachable at. (e.g. "https://umc-server")</td>
		</tr>
		<tr>
			<td>waitForDependency.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus/images/wait-for-dependency"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"0.35.27@sha256:3f9f37e224a7a8e268ee2cdf1ca8d18826d2d0d5b356a2a5a3cbfa4968a2a281"
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>

