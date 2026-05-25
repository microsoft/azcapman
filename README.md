# Azure quota and capacity management documentation

This repository contains Azure quota and capacity management references for SaaS ISVs that operate workloads in subscriptions owned or controlled by the ISV (Enterprise Agreement or Microsoft Customer Agreement), not in customer-owned subscriptions.

> [!NOTE]
> This repository provides an addendum to the ISV landing zone guidance and complements the Azure Cloud Adoption Framework and Well-Architected guidance for ISVs operating on Azure.[^isv-landing-zone]

## 📖 Documentation

View the documentation at: **https://microsoft.github.io/azcapman/**

The documentation is organized into:

- **[Deployment](docs/deployment/)** - ISV deployment patterns (single-tenant vs multi-tenant)
- **[Billing](docs/billing/)** - EA vs MCA billing guidance
- **[Operations](docs/operations/)** - Quota, capacity, monitoring, and automation references
- **[Glossary](docs/operations/glossary.md)** - Key terms and concepts

## 🚀 Quick Start

All documentation is in pure Markdown format in the `docs/` directory. Browse locally or view on GitHub Pages.

## Structure

- `docs/` — Markdown documentation with citations to Microsoft Learn
  - `docs/billing/` — Billing guidance (modern MCA and legacy EA)
  - `docs/deployment/` — ISV deployment guides
  - `docs/operations/` — Operations references for quota and capacity management
- `scripts/` — PowerShell and Python scripts for quota, capacity, and rate optimization
- `.github/workflows/` — GitHub Pages deployment automation

All documentation includes citations to official Microsoft Learn sources.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Security

For security concerns, see [SECURITY.md](SECURITY.md). Don't report security vulnerabilities through public GitHub issues.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

---

[^isv-landing-zone]: [Independent software vendor (ISV) considerations for Azure landing zones](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/isv-landing-zone)
