# GitHub Pages

The [Pages workflow](../.github/workflows/pages.yaml) builds and deploys on pushes to `main`. It can also be started from the Actions tab. Manual runs on other branches build only; deployment is restricted to `main`.

## Enable once

In the GitHub repository, open **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**. Commit and push the workflow when ready. No personal token or Docker registry credentials are needed; deployment uses GitHub's built-in token.

The build does not require Pages to be enabled. While Pages is unavailable for this repository, asset generation, compilation, tests and the website artifact upload can still complete. Only the final deployment job is expected to fail; the uploaded website artifact remains downloadable from the workflow run for seven days. Once Pages becomes available, enable it and rerun the workflow.

For `s-macke/maniac-mansion-3d`, the default website address is:

<https://s-macke.github.io/maniac-mansion-3d/>

## Build and deployment

The workflow uses the existing Dockerfile and `scripts/build.py` to generate the shared doors, all rooms, baked lighting, compact GLBs, inventories and previews. It then installs locked npm dependencies, compiles the static website, typechecks it and runs the Dockerfile's focused navigation and GLB tests. A failed build or test prevents deployment.

The website uses relative asset URLs, so one build works at the repository Pages path, a custom-domain root, or any nested folder. No repository-name lookup, Pages API query, or base-path variable is needed. The Docker `pages` target exports only `web/dist/client/`; Blender scenes, reports, source artwork and npm dependencies are not uploaded as site files. The ignored connection drawing is not a build dependency.

BuildKit's GitHub Actions cache retains intermediate layers, including baked models. The first build can take tens of minutes; source changes invalidate the relevant layers. A manual run offers **Rebuild all Blender assets even if cached** to force the models stage. Builds have a three-hour timeout and deployments are serialized.

## Reproduce locally

```bash
docker buildx build --platform linux/amd64 --target pages \
  --output type=local,dest=exports/pages .
```

Serve these same files at `/`, `/maniac-mansion-3d/`, or another folder. Directory URLs must end in `/` or redirect there; direct `index.html` access also works. Existing Compose commands and the full `artifacts` export continue to work.

The workflow itself must run on GitHub to verify repository permissions and deployment. Local compilation and navigation tests do not verify physical mobile performance.

See GitHub's [custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and Docker's [GitHub Actions cache documentation](https://docs.docker.com/build/cache/backends/gha/).
