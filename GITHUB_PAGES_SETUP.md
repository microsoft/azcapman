# GitHub Pages setup instructions

This repository is configured to automatically deploy documentation to GitHub Pages using DocFX.

## Enable GitHub Pages

1. **Push your changes to GitHub**:
   ```bash
   git push origin main
   ```

2. **Enable GitHub Pages in repository settings**:
   - Go to your repository on GitHub: https://github.com/msbrett/azcapman
   - Click on **Settings** tab
   - Scroll down to **Pages** section in the left sidebar
   - Under **Source**, select **GitHub Actions**

3. **Wait for the first deployment**:
   - The GitHub Actions workflow will automatically trigger on push to main branch
   - Go to the **Actions** tab to monitor the deployment progress
   - The workflow is named "Deploy DocFX to GitHub Pages"

4. **Access your documentation**:
   - Once deployed, your documentation will be available at:
   - https://msbrett.github.io/azcapman/

## Local Development

To run the documentation site locally:

1. **Install DocFX**:
   ```bash
   dotnet tool install -g docfx
   ```

2. **Build the documentation**:
   ```bash
   docfx build
   ```

3. **Serve locally**:
   ```bash
   docfx serve _site --port 8080
   ```

4. **View the site**:
   - Open http://localhost:8080 in your browser

## Workflow Details

The GitHub Actions workflow (`.github/workflows/docfx-gh-pages.yml`):
- Triggers on pushes to the main branch
- Installs .NET and DocFX
- Builds the documentation
- Deploys to GitHub Pages

## Troubleshooting

If the deployment fails:

1. Check the Actions tab for error messages
2. Ensure GitHub Pages is enabled with "GitHub Actions" as the source
3. Verify the repository has the necessary permissions for Pages deployment
4. Check that the DocFX build succeeds locally before pushing

## Documentation Structure

- `/docs/` - Source markdown files
- `/docs/toc.yml` - Main table of contents
- `/docfx.json` - DocFX configuration
- `/_site/` - Built output (git-ignored)

The site uses Microsoft's DocFX with the default/modern theme for a professional, Microsoft Learn-style appearance.
