# Portfolio design system

## Identity
Jack Ormston — Data Science · Analytics · Engineering.
Use an editorial scientific-publication aesthetic: serif titles, sans-serif metadata, restrained graphics and generous spacing. Avoid animated typing, badge walls and decorative AI imagery.

## Palette
| Colour | Hex | Role |
| --- | --- | --- |
| Parchment | #F1EBDD | Light background |
| Forest | #253D35 | Primary ink and literary project |
| Terracotta | #BB785A | Accent and document project |
| Slate | #82969D | Forecasting and secondary graphics |
| Charcoal | #292B2D | Production ML and dark ink |

## Project assets
| Project | Banner | Background |
| --- | --- | --- |
| 01 Literary Character Network Intelligence | [SVG](../assets/projects/literary-network.svg) | Forest |
| 02 Retail Analytics Data Platform | [SVG](../assets/projects/retail-analytics.svg) | Parchment |
| 03 Demand Forecasting | [SVG](../assets/projects/demand-forecasting.svg) | Slate |
| 04 Document Intelligence Assistant | [SVG](../assets/projects/document-intelligence.svg) | Terracotta |
| 05 Production ML & Monitoring | [SVG](../assets/projects/production-ml.svg) | Charcoal |

All banners are editable 1200 × 310 SVGs. Graphics are illustrative, not measured results. Copy the relevant asset into each project's own assets/banner.svg and reference it using a relative Markdown image link with meaningful alt text. Check rendered text and contrast in GitHub light and dark modes and on mobile before release.

## Documentation and engineering standards
Start from the [README template](../templates/project-readme.md), adapt sections to the project, and remove unused placeholders. Prefer a short personal motivation and concrete findings over marketing language. Use actual screenshots, diagrams and measured results.

For Python projects, use a documented environment and pinned or locked dependencies, a src/ package, tests/, and clear scripts or CLI entry points. Keep raw data immutable, record provenance and licences, and exclude secrets and restricted data. Use .env.example where configuration is required. Add automated tests and CI where appropriate. Document how to reproduce results and record important methodological decisions. Adapt these conventions to SQL and BI projects rather than imposing a Python structure on them.

## Publication checklist
- [ ] README accurately distinguishes implemented and planned work
- [ ] Data sources and licences documented
- [ ] Setup and evaluation reproducible
- [ ] Tests run and results recorded
- [ ] Limitations and baseline comparisons included where relevant
- [ ] No confidential data, credentials or private employer material
- [ ] Banner and screenshots checked in light and dark modes
- [ ] Repository description and topics reflect actual work
