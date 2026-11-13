# Evidence register

Secondary-source portfolio analysis. ATT&CK mappings are analyst judgments.
Confidence concerns our claim, not a numerical probability.

## E01
Microsoft описывает HTML-вложение с приманкой голосового сообщения и последующими перенаправлениями.

Source: [S1](https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/); section: Initial access.
Kind: reported_observation; confidence: medium; mapping: [T1566.001](https://attack.mitre.org/techniques/T1566/001/).

## E02
В описанном потоке AiTM перехватывает пароль и session cookie.

Source: [S1](https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/); section: Tracking an AiTM phishing campaign.
Kind: reported_observation; confidence: medium; mapping: [T1539](https://attack.mitre.org/techniques/T1539/).

## E03
Автор публикации связывает инфраструктуру исследованных итераций с Evilginx2.

Source: [S1](https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/); section: Tracking an AiTM phishing campaign.
Kind: reported_observation; confidence: medium; mapping: [T1557](https://attack.mitre.org/techniques/T1557/).

## E04
После компрометации Microsoft наблюдал доступ к почте и попытки платёжного мошенничества.

Source: [S1](https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/); section: Post-breach BEC.
Kind: reported_observation; confidence: medium; mapping: not mapped.

## Source register

- [S1 — Microsoft: From cookie theft to BEC](https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/); published: 2022-07-12; accessed: 2026-11-13. Один поставщик телеметрии; независимых первичных данных в проекте нет.
- [S2 — MITRE ATT&CK T1539: Steal Web Session Cookie](https://attack.mitre.org/techniques/T1539/); published: not recorded; accessed: 2026-11-13. Описание техники, не независимое подтверждение кампании.
- [S3 — MITRE ATT&CK T1557: Adversary-in-the-Middle](https://attack.mitre.org/techniques/T1557/); published: not recorded; accessed: 2026-11-13. Общая техника; mapping аналитический.
- [S4 — MITRE ATT&CK T1566.001: Spearphishing Attachment](https://attack.mitre.org/techniques/T1566/001/); published: not recorded; accessed: 2026-11-13. Сопоставление HTML-вложения — аналитическая классификация.
