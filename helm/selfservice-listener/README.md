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
| oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/common-helm/helm | common | ^0.3.0 |

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
			<td>autoscaling.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
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
			<td>Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry"</td>
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
			<td>ldap.credentialSecret.ldapPasswordKey</td>
			<td>string</td>
			<td><pre lang="json">
"ldap.secret"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldap.credentialSecret.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldap.tlsSecret.caCertKey</td>
			<td>string</td>
			<td><pre lang="json">
"ca.crt"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldap.tlsSecret.certificateKey</td>
			<td>string</td>
			<td><pre lang="json">
"tls.crt"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldap.tlsSecret.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldap.tlsSecret.privateKeyKey</td>
			<td>string</td>
			<td><pre lang="json">
"tls.key"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>mountSecrets</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
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
			<td>persistence.data.size</td>
			<td>string</td>
			<td><pre lang="json">
"1Gi"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>persistence.data.storageClass</td>
			<td>string</td>
			<td><pre lang="json">
""
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
			<td>probes.liveness.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.liveness.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.liveness.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
120
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.liveness.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
30
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.liveness.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.liveness.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.readiness.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.readiness.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
30
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.readiness.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
30
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.readiness.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.readiness.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.readiness.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
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
			<td>Deployment resources for the listener container</td>
		</tr>
		<tr>
			<td>resourcesWaitForDependency</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Deployment resources for the dependency waiters</td>
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
			<td>selfserviceInvitation.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceInvitation.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus/images/selfservice-invitation"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceInvitation.image.sha256</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Define image sha256 as an alternative to `tag`</td>
		</tr>
		<tr>
			<td>selfserviceInvitation.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.caCert</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>CA root certificate, base64-encoded. Optional; will be written to "caCertFile" if set.</td>
		</tr>
		<tr>
			<td>selfserviceListener.caCertFile</td>
			<td>string</td>
			<td><pre lang="json">
"/run/secrets/ca_cert"
</pre>
</td>
			<td>Where to search for the CA Certificate file.</td>
		</tr>
		<tr>
			<td>selfserviceListener.certPem</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.debugLevel</td>
			<td>string</td>
			<td><pre lang="json">
"4"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.environment</td>
			<td>string</td>
			<td><pre lang="json">
"production"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus/images/selfservice-listener"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.image.sha256</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Define image sha256 as an alternative to `tag`</td>
		</tr>
		<tr>
			<td>selfserviceListener.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapBaseDn</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapHost</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapHostDn</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapPort</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Will add a mapping from "ldapHost" to "ldapHostIp" into "/etc/hosts" if set</td>
		</tr>
		<tr>
			<td>selfserviceListener.ldapSecretFile</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/ldap_secret"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.notifierServer</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Defaults to "ldapHost" if not set.</td>
		</tr>
		<tr>
			<td>selfserviceListener.secretMountPath</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.tlsMode</td>
			<td>string</td>
			<td><pre lang="json">
"off"
</pre>
</td>
			<td>Whether to start encryption and validate certificates. Chose from "off", "unvalidated" and "secure".</td>
		</tr>
		<tr>
			<td>selfserviceListener.umcAdminPasswordSecret.key</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.umcAdminPasswordSecret.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.umcAdminUser</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>selfserviceListener.umcServerUrl</td>
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
"0.25.0"
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>

