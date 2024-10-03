# Changelog

## [0.11.2](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.11.1...v0.11.2) (2024-10-03)


### Bug Fixes

* removed unused functions on the template helper ([4777295](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/4777295b56736eb8a89b51d43dd1477fc135f5db))

## [0.11.1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.11.0...v0.11.1) (2024-09-26)


### Bug Fixes

* bump Provisioning client version, adapt to new subscriptions format ([97d29bf](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/97d29bf6139f7a0756cf082efe8aa44a212321c2))

## [0.11.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.10.0...v0.11.0) (2024-09-26)


### Features

* **ci:** enable malware scanning, disable sbom generation ([f146042](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/f1460428eeda3081ade42cbc4eceac7ec1561b7c))

## [0.10.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.9.1...v0.10.0) (2024-09-24)


### Features

* bump provisioning client, adapt to new endpoint names ([744e66e](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/744e66e1c8e9341290fcde042250c1a0670316da))

## [0.9.1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.9.0...v0.9.1) (2024-09-23)


### Bug Fixes

* Don't leak secrets in bash scripts ([adc70c9](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/adc70c9a95921414d7a4d551c4e00c5cf7f61399))

## [0.9.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.8.0...v0.9.0) (2024-09-18)


### Features

* remove umc admin credentials ([dcd299d](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/dcd299d0a75e3502765ff6c83ea8c29ec4110de7))

## [0.8.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.7.3...v0.8.0) (2024-09-16)


### Features

* update UCS base image to 2024-09-09 ([67849b7](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/67849b7f2bce8b50bf9b334a994bbed86512fe70))
* upgrade wait-for-dependency ([7e141c6](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/7e141c6997a27bbed07f40a34ff15059aad65432))

## [0.7.3](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.7.2...v0.7.3) (2024-09-12)


### Bug Fixes

* add wait-for-provisioning-api to wait until the user/subscription is created ([6b2014a](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/6b2014a0b2b7e6a416a0d7fdfbc28fa05a38f54f))

## [0.7.2](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.7.1...v0.7.2) (2024-08-29)


### Bug Fixes

* update nubus-provisioning-consumer to use ProvisioningMessage model ([3c7cdcd](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/3c7cdcd8605aed1611b9f899f0337aa4e90a0205))

## [0.7.1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.7.0...v0.7.1) (2024-08-21)


### Bug Fixes

* rename helm chart from listener to consumer ([fceb5b7](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/fceb5b74b94071f8c77deae92667555f7d6d379f))

## [0.7.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.6.5...v0.7.0) (2024-08-14)


### Features

* update nubus-provisioning-consumer lib to use Body model ([de0e85f](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/de0e85fddc36dcfc33d1ff64dff2affaa82aa1b6))


### Bug Fixes

* add new config values to the helm chart ([cfc10c1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/cfc10c1e6ef1e03b52204d93aad96cc1467d2010))
* add pydantic to the python dependencies ([57dcf0b](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/57dcf0b2a1c10ebdcf763e0cc6421b7918721909))
* cleanup ([5752cdb](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/5752cdb1047de7512e2f42a6d43d00fab15c7c1d))
* don't sleep after the last retry, but fail immediately ([39775d3](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/39775d38b4e1b191a519cc5b7c8613692a7b4eb3))
* UMC 503 errors throw exceptions when trying to read the response message ([0272d25](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/0272d25a426c2e0b058f59e629d69b708ba69146))
* update is_create_event method to handle empty dictionaries ([fe97e48](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/fe97e4847827a980e50799439d4bcb9d42663f1f))
* update nubus-provisioning-consumer lib version ([c552d86](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/c552d867c7af1e5ebf4bba8307273c61955c1941))
* update secret handling to selfservice-consumer requirements ([15e2052](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/15e20527d4be493bdfabf2cef46f7db2128cfee3))


### Reverts

* "fix: secret handling and nubus umbrella integration" ([507318c](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/507318c9c20fcfebb90b93f91bce7a53f6e4aa25))
* "revert: provisioning to listener/notifier" ([00326cf](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/00326cf6edfd2cab78655b22cee5ee448bfb8c16))

## [0.6.5](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.6.4...v0.6.5) (2024-07-30)


### Bug Fixes

* fix containers name ([f86159e](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/f86159e14c427b397db9cf0497f90fcc4f31be77))
* missing configuration for machine.secret ([2c73e11](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/2c73e11e40d15686f1c7cbc7c258269cadff5e21))
* UMC credentials ([1f758d2](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/1f758d2217b6bbeb118e793bd9ff5ac8180db1e3))
* UMC crendentials in wrong container ([45ee29d](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/45ee29dd0a52da9d19957048c1e0039849c577f3))
* use LDAP primary and remove machine.secret ([4be43bd](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/4be43bdee982ba5090e119ea2b645ea0d525ddbc))

## [0.6.4](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.6.3...v0.6.4) (2024-07-24)


### Bug Fixes

* secret handling and nubus umbrella integration ([7547032](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/75470323e01158056d79826b684b891019eec926))


### Reverts

* provisioning to listener/notifier ([9f4f81d](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/9f4f81dd9d442627c38548a2186c0cbf71cfd8ce))

## [0.6.3](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.6.2...v0.6.3) (2024-07-11)


### Bug Fixes

* remove the env | sort from the consumer entrypoints ([18a1938](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/18a1938ae8c7d28933b49022f7ef8065feca7e46))

## [0.6.2](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.6.1...v0.6.2) (2024-05-23)


### Bug Fixes

* use global registry ([dd5b08a](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/dd5b08a656045abab315958a44bc63ba5a016322))

## [0.6.1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.6.0...v0.6.1) (2024-05-23)


### Bug Fixes

* README ([52f2819](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/52f281938393619772dcf6c58dc13739c28eeffc))

## [0.6.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.5.0...v0.6.0) (2024-05-22)


### Features

* changes to support the refactored umbrella values in a nubus deployment ([cf02cb6](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/cf02cb67df469de2a9ca0b350c0353de7281554e))

## [0.5.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.4.1...v0.5.0) (2024-05-15)


### Features

* implement new retry logic ([31ba1eb](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/31ba1eb5a4dd3cd8c9b9cd49670b31de513cc29e))
* run tests in the pipeline, add timeout to the ClientSession, fix tests ([a908b2e](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/a908b2ec0d10ee239e911e6ff804536313c57273))
* update helm chart to use only selfservice invitation, add new filters for incoming messages, remove listener ([8cbe361](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/8cbe36166ab17c797f8b0af03c157009f79d146d))
* use provisioning-consumer-lib to listen for newly created users ([d0565a7](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/d0565a7286ccaad1036ce013a18bc7db683adc34))


### Bug Fixes

* add license headers to the test file and fix helm README ([d255fe8](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/d255fe8f3cf15282fba904e9f8ad36d2ebff1d72))
* add pyproject.toml, refactor selfservice invitation Dockerfile, add pre-commit hooks, remove selfservice-listener from the gitlab-ci ([c28dd42](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/c28dd424575a7d8d419d8cc14630794e69252a02))
* add sleep intervals between retries when sending emails, fix test ([035c8c8](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/035c8c8042ab80361566c2f19180973c47bba96e))
* change fields for filtering messages ([9f2a292](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/9f2a29256d6ac4b08e8d3a7a015799a2d372941a))
* do not register consumer, update provisioning lib ([e59b502](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/e59b502fc5d46b52f75cf6a3f8537dd6ed92c75a))
* let pydantic_settings read the env values and AsyncClient instantiate the Settings class ([7f5f45e](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/7f5f45e295c2b5d559afbe5da4b6174a5fa1aaa6))
* rename provisioning credentials ([8d177a8](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/8d177a857123039e5577ab4142601f79b0add86c))
* replace the synchronous 'requests' with aiohttp, add constant for MAX_RETRIES ([4ae602c](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/4ae602c153ce8a7525163c6d71d032a4a696c3bb))
* use a single 'with' statement with multiple contexts for sending emails, add annotations, fix UMC server error handling ([7166cd1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/7166cd1c291916572ecdaddbc3e719b4b7270c36))
* use exponential back-off for retry ([6ca86bb](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/6ca86bb846bd9e2c743c088a407cdeb3bf1c82bb))

## [0.4.1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.4.0...v0.4.1) (2024-05-07)


### Bug Fixes

* Update base image to version 0.12.0 ([d79d194](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/d79d194d137d79a76b42156778294a3cb5123ef1))
* Update listener base image to version 0.7.0 ([3cc36a2](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/3cc36a29cd57857e8889df01e7c73c0f4d7d8029))

## [0.4.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.3.2...v0.4.0) (2024-03-26)


### Features

* **ci:** add debian update check jobs for scheduled pipeline ([f3419c6](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/f3419c61940b1556c3c033fde88c47cb890284d5))


### Bug Fixes

* **ci:** update common-ci from v1.16.1 to v1.25.0 ([05f926a](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/05f926ac6f91572cd258ba304ed21024f904748b))
* **deps:** add renovate.json ([0f0bdf0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/0f0bdf0b1519905ba1415f855fba1407d4be38a5))
* **license:** add missing license headers, replace pre-commit licensing hook ([bf0855a](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/bf0855a361413842ea1cbf8f611040f14e75a4d9))

## [0.3.2](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.3.1...v0.3.2) (2023-12-21)


### Bug Fixes

* **docker:** bump version to UCS 5.0-6 ([2abc091](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/2abc09170f3276753cb5be785b20090232774cf4))

## [0.3.1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.3.0...v0.3.1) (2023-12-18)


### Bug Fixes

* **ci:** add Helm chart signing and publishing to souvap via OCI, common-ci 1.12.x ([329726e](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/329726e07f22b602a63fa635ffcc567dbbae4fc7))

## [0.3.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.2.0...v0.3.0) (2023-12-12)


### Features

* **invitation:** Refactor to enable maximum retries of 5 ([ff5b395](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/ff5b395ef48be93b46cc738d8e08e81ad1d2e011))

## [0.2.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.1.1...v0.2.0) (2023-12-12)


### Features

* **invitation:** Add selfservice invitation container ([d1ff470](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/d1ff47044dd67233a455fd8012324b6e56847929))

## [0.1.1](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.1.0...v0.1.1) (2023-12-11)


### Bug Fixes

* **listener:** use the same ldap filter as upstream ([c124b2c](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/c124b2cc74f045df536d5de6c678c0e564821b9e))

## [0.1.0](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.0.2...v0.1.0) (2023-12-08)


### Features

* **listener:** ensure cache volume permissions ([c9a0886](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/c9a088667624c2be8d0985b699c274e8f5446222))

## [0.0.2](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/compare/v0.0.1...v0.0.2) (2023-12-07)


### Bug Fixes

* **listener:** change cache directory ([e8622fa](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/e8622fa65333e57ced39c7093f11d08465b20255))

## 0.0.1 (2023-12-07)


### Features

* **ci:** setup repository pipeline ([cec6d82](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/cec6d8299068d02a0e6a8865cd1743c7b6ffdc66))
* **docker:** selfservice-listener image ([9b67773](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/9b67773bd23e99ee074a58eed2cf9c98bea00c67))
* **helm:** selfservice-listener chart ([db24b4c](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/db24b4c75781e378d4216cd32e9eebd70dad9bde))
* **listener:** selfservice listener ([fbab462](https://git.knut.univention.de/univention/customers/dataport/upx/selfservice-listener/commit/fbab462e09368d4d4b264fe6b855a5060c166333))
