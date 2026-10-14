const prefix = 'daily-briefs-';

function validDate(value) {
  return /^\d{4}-\d{2}-\d{2}$/.test(value)
    && Number.isFinite(Date.parse(`${value}T00:00:00Z`))
    && new Date(`${value}T00:00:00Z`).toISOString().slice(0, 10) === value;
}

module.exports = async ({ github, context, core, date }) => {
  const repo = context.repo;
  const sourceRun = context.eventName === 'workflow_run'
    ? context.payload.workflow_run.id : undefined;
  if (!sourceRun && !validDate(date)) {
    throw new Error(`Invalid brief date: ${date}. Expected YYYY-MM-DD.`);
  }

  const artifacts = sourceRun
    ? await github.paginate(github.rest.actions.listWorkflowRunArtifacts, {
      ...repo, run_id: sourceRun, per_page: 100,
    })
    : await github.paginate(github.rest.actions.listArtifactsForRepo, {
      ...repo, name: `${prefix}${date}`, per_page: 100,
    });
  const candidates = artifacts.filter(artifact => !artifact.expired && (
    sourceRun
      ? artifact.name.startsWith(prefix) && validDate(artifact.name.slice(prefix.length))
      : artifact.name === `${prefix}${date}`
  )).sort((a, b) => b.id - a.id);

  for (const artifact of candidates) {
    const runId = sourceRun || artifact.workflow_run?.id;
    if (!runId) continue;
    const { data: run } = await github.rest.actions.getWorkflowRun({
      ...repo, run_id: runId,
    });
    if (run.conclusion !== 'success' || run.head_branch !== 'main'
      || run.path !== '.github/workflows/daily-briefs.yml'
      || run.head_repository?.full_name !== `${repo.owner}/${repo.repo}`) continue;

    const contentDate = artifact.name.slice(prefix.length);
    core.setOutput('run_id', String(runId));
    core.setOutput('artifact_name', artifact.name);
    core.setOutput('date', contentDate);
    core.info(`Using ${artifact.name} from successful Daily Tech Briefs run ${runId}`);
    return;
  }
  throw new Error(
    `No unexpired Daily Tech Briefs artifact from a successful main run for ${
      sourceRun ? `source run ${sourceRun}` : date
    }. Generate the requested briefs before retrying the upload.`,
  );
};
