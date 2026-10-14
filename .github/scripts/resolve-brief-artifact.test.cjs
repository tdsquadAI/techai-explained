const assert = require('node:assert/strict');
const { test } = require('node:test');
const resolve = require('./resolve-brief-artifact.cjs');

function fixture({ event = 'schedule', date = '2026-10-11', artifacts, run = {} } = {}) {
  const outputs = {};
  const listWorkflowRunArtifacts = {};
  const listArtifactsForRepo = {};
  const calls = [];
  const args = {
    date,
    context: {
      repo: { owner: 'brand', repo: 'techai-explained' },
      eventName: event,
      payload: { workflow_run: { id: 42 } },
    },
    core: {
      setOutput: (key, value) => { outputs[key] = value; },
      info: () => {},
    },
    github: {
      paginate: async (endpoint, params) => {
        calls.push({ endpoint, params });
        return artifacts ?? [{
          id: 10, name: 'daily-briefs-2026-10-11', expired: false,
          workflow_run: { id: 42 },
        }];
      },
      rest: {
        actions: {
          listWorkflowRunArtifacts,
          listArtifactsForRepo,
          getWorkflowRun: async ({ run_id }) => {
            calls.push({ run_id });
            return { data: {
              conclusion: 'success', head_branch: 'main',
              path: '.github/workflows/daily-briefs.yml',
              head_repository: { full_name: 'brand/techai-explained' },
              ...run,
            } };
          },
        },
      },
    },
  };
  return { args, outputs, calls, listWorkflowRunArtifacts, listArtifactsForRepo };
}

for (const event of ['schedule', 'workflow_dispatch']) {
  test(`${event} resolves the explicit source run and named artifact`, async () => {
    const f = fixture({ event });
    await resolve(f.args);
    assert.equal(f.calls[0].endpoint, f.listArtifactsForRepo);
    assert.equal(f.calls[0].params.name, 'daily-briefs-2026-10-11');
    assert.deepEqual(f.outputs, {
      run_id: '42', artifact_name: 'daily-briefs-2026-10-11', date: '2026-10-11',
    });
  });
}

test('workflow_run preserves the source artifact date across midnight', async () => {
  const f = fixture({ event: 'workflow_run', date: '2026-10-12' });
  await resolve(f.args);
  assert.equal(f.calls[0].endpoint, f.listWorkflowRunArtifacts);
  assert.equal(f.calls[0].params.run_id, 42);
  assert.equal(f.outputs.date, '2026-10-11');
});

for (const date of ['2026-02-30', '2026-13-01', '11-10-2026', '']) {
  test(`rejects invalid date ${JSON.stringify(date)}`, async () => {
    const f = fixture({ date });
    await assert.rejects(resolve(f.args), /Invalid brief date/);
    assert.equal(f.calls.length, 0);
  });
}

for (const artifacts of [
  [],
  [{ id: 10, name: 'daily-briefs-2026-10-11', expired: true }],
  [{ id: 10, name: 'daily-briefs-2026-10-10', expired: false }],
]) {
  test(`fails explicitly for unavailable requested artifact ${JSON.stringify(artifacts)}`, async () => {
    const f = fixture({ artifacts });
    await assert.rejects(resolve(f.args), /No unexpired Daily Tech Briefs artifact/);
    assert.deepEqual(f.outputs, {});
  });
}

for (const run of [
  { conclusion: 'failure' },
  { head_branch: 'feature' },
  { path: '.github/workflows/other.yml' },
  { head_repository: { full_name: 'fork/techai-explained' } },
]) {
  test(`rejects untrusted or unsuccessful source ${JSON.stringify(run)}`, async () => {
    const f = fixture({ run });
    await assert.rejects(resolve(f.args), /No unexpired Daily Tech Briefs artifact/);
    assert.deepEqual(f.outputs, {});
  });
}

test('selects the newest matching artifact when a date was regenerated', async () => {
  const f = fixture({ artifacts: [
    { id: 10, name: 'daily-briefs-2026-10-11', workflow_run: { id: 42 } },
    { id: 20, name: 'daily-briefs-2026-10-11', workflow_run: { id: 43 } },
  ] });
  await resolve(f.args);
  assert.equal(f.outputs.run_id, '43');
});

test('workflow_run cannot fall back to artifacts from another run', async () => {
  const f = fixture({ event: 'workflow_run', artifacts: [] });
  await assert.rejects(resolve(f.args), /source run 42/);
  assert.equal(f.calls.length, 1);
});

test('workflow_run rejects expired source artifacts', async () => {
  const f = fixture({ event: 'workflow_run', artifacts: [
    { id: 10, name: 'daily-briefs-2026-10-11', expired: true },
  ] });
  await assert.rejects(resolve(f.args), /source run 42/);
  assert.deepEqual(f.outputs, {});
});

test('skips artifacts from failed runs when an older successful run is available', async () => {
  const f = fixture({ artifacts: [
    { id: 20, name: 'daily-briefs-2026-10-11', workflow_run: { id: 43 } },
    { id: 10, name: 'daily-briefs-2026-10-11', workflow_run: { id: 42 } },
  ] });
  const getRun = f.args.github.rest.actions.getWorkflowRun;
  f.args.github.rest.actions.getWorkflowRun = async params => {
    const result = await getRun(params);
    if (params.run_id === 43) result.data.conclusion = 'failure';
    return result;
  };
  await resolve(f.args);
  assert.equal(f.outputs.run_id, '42');
});
