#### Detection Rules: Ideas & Resources
Microsoft Sentinel Analytic Rules
- https://analyticsrules.exchange/

Sigma Emerging threat rules  
- https://github.com/SigmaHQ/sigma/tree/master/rules-emerging-threats  

Sigma Rules:  
- https://github.com/SigmaHQ/sigma/tree/master/rules  

Detections & Ideas:  
- https://detections.ai/

OpenSIEM    
We are building the first dedicated platform for sharing and organising high-quality SIEM content — from detection rules and playbooks to dashboards and automation workflows.
- https://www.opensiem.ai/  
FortiSIEM Rules
- https://filestore.fortinet.com/docs.fortinet.com/fsiem/Public_Resource_Access/7_1_1/rules/rule_descriptions.htm  

Splunk Detections  
- https://research.splunk.com/detections/  


Panther Detections  
- https://github.com/panther-labs/panther-analysis  

DataDogHQ Detections  
- https://docs.datadoghq.com/security/detection_rules/
- https://docs.datadoghq.com/security/default_rules/

Stellar Cyber
- https://docs.stellarcyber.ai/4.3.x/Using/ML/Alert-Rule-Based-Intro.htm

Elastic Detections  
- https://github.com/elastic/detection-rules

Cortex XDR analytics alert references:  
- https://docs-cortex.paloaltonetworks.com/r/Cortex-XDR/Cortex-XDR-Analytics-Alert-Reference-by-data-source/Cortex-XDR-Analytics-Alert-Reference


#### Detection Engineering Maturity Matrix  
- https://detectionengineering.io/  


#### SOC Automation Capability Matrix  
- https://tinesio.notion.site/4fd14ccf93e7408c8faf96c5aca8c3fd?v=6c62326a57444ca9890e41daad193e3c
- https://tuckner.github.io/automation-capability-matrix/  

#### Microsoft Teams Threat Matrix 
- https://cyberdom.blog/inside-the-microsoft-teams-attack-matrix-unpacking-the-the-frontier-in-collaboration-threats/

## Log Collection
#### Log Events - Trend Micro
- https://help.deepsecurity.trendmicro.com/10/0/Events-Alerts/syslog-parsing.html
- https://docs.trendmicro.com/en-us/documentation/article/trend-vision-one-syslog-content-mapping-cef

Windows Events Collection Guide  Yamato Security
- https://github.com/Yamato-Security/EnableWindowsLogSettings/tree/main

CISCO ISE   
ISE Syslog Messages-Message codes and their description.  
- https://www.cisco.com/c/en/us/td/docs/security/ise/syslog/Cisco_ISE_Syslogs/m_SyslogsList.html
what events to collect?
- https://docs.sophos.com/central/customer/help/en-us/ManageYourProducts/ThreatAnalysisCenter/Integrations/Cisco/ISE/index.html#allow



Malware analysis: 
- https://ohmymalware.com/ 

OSSEM  
- https://github.com/OTRF/OSSEM

## DDOS

DDOS: State of IP Spoofing
- https://spoofer.caida.org/summary.php
- https://www.microsoft.com/en-us/security/blog/2022/05/23/anatomy-of-ddos-amplification-attacks/







Lols:  
- https://boostsecurityio.github.io/lotp/






Adversarial Detection Engineering Framework
- https://adeframework.org/

Detection Logic Bugs:
- 

Detection backlog:
- https://specterops.io/blog/2022/10/05/prioritization-of-the-detection-engineering-backlog/?source=rss----f05f8696e3cc---4




Opensearch:  
The pySigma-backend-opensearch repo provides the OpensearchLuceneBackend class. It supports converting Sigma rules into Lucene queries and OpenSearch Monitor Rules (alerting rules). The PPL backend is implemented from scratch to support OpenSearch's native Piped Processing Language, including full support for Sigma correlation rules (event_count, value_count, temporal patterns)
- https://github.com/SigmaHQ/pySigma-backend-opensearch




