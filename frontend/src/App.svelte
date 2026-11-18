<script>
	let datasets = [];
	let name = '';
	let rows = 0;
	let uploadResult = null;
	let selectedFile = null;
	let isUploading = false;
	let deletingId = null;

	async function loadDatasets() {
		const response = await fetch('http://localhost:8000/datasets');
		datasets = await response.json();
	}

	async function createDataset() {
		if (!name.trim()) return;

		await fetch('http://localhost:8000/datasets', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name: name.trim(), rows: Number(rows) || 0 })
		});

		await loadDatasets();
		name = '';
		rows = 0;
	}

	async function deleteDataset(id) {
		deletingId = id;
		await fetch(`http://localhost:8000/datasets/${id}`, { method: 'DELETE' });
		await loadDatasets();
		deletingId = null;
	}

	async function uploadCsv(event) {
		const file = event.target.files?.[0];
		if (!file) return;

		selectedFile = file;
		isUploading = true;
		uploadResult = null;

		const formData = new FormData();
		formData.append('file', file);

		const response = await fetch('http://localhost:8000/upload', {
			method: 'POST',
			body: formData
		});

		const result = await response.json();
		uploadResult = response.ok ? result : { error: result.detail };
		isUploading = false;

		if (response.ok) {
			await loadDatasets();
			event.target.value = '';
			selectedFile = null;
		}
	}

	$: totalRows = datasets.reduce((total, dataset) => total + (Number(dataset.rows) || 0), 0);

	loadDatasets();
</script>

<main class="min-h-screen bg-base-200 text-base-content">
	<header class="border-b border-base-300 bg-base-100">
		<div class="navbar mx-auto max-w-7xl px-6">
			<div class="flex-1 gap-3">
				<div class="grid size-11 place-items-center rounded-xl bg-primary text-xl font-black text-primary-content shadow-lg">
					D
				</div>
				<div>
					<p class="text-[10px] font-black tracking-[0.18em] text-base-content/50">DATA PLATFORM</p>
					<h1 class="text-lg font-bold">Datasets</h1>
				</div>
			</div>
		</div>
	</header>

	<section class="mx-auto max-w-7xl px-6 py-10">
		<div class="mb-6 flex flex-wrap items-end justify-between gap-4">
			<div>
				<p class="text-xs font-black tracking-[0.18em] text-base-content/50">OVERVIEW</p>
				<h2 class="text-4xl font-black tracking-tight">Your datasets</h2>
			</div>
			<label for="csv-file" class="btn btn-primary gap-2 shadow-lg">
				<svg class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 14v4a2 2 0 002 2h10a2 2 0 002-2v-4" />
				</svg>
				{isUploading ? 'Uploading...' : 'Upload CSV'}
			</label>
			<input id="csv-file" class="hidden" type="file" accept=".csv,text/csv" on:change={uploadCsv} />
		</div>

		<div class="mb-4 grid gap-4 sm:grid-cols-3">
			<div class="stats border border-base-300 bg-base-100 shadow-sm">
				<div class="stat">
					<div class="stat-title">Datasets</div>
					<div class="stat-value text-primary">{datasets.length}</div>
				</div>
			</div>
			<div class="stats border border-base-300 bg-base-100 shadow-sm">
				<div class="stat">
					<div class="stat-title">Total rows</div>
					<div class="stat-value text-secondary">{totalRows.toLocaleString()}</div>
				</div>
			</div>
			<div class="stats border border-base-300 bg-base-100 shadow-sm">
				<div class="stat">
					<div class="stat-title">Storage</div>
					<div class="stat-value text-success">S3</div>
				</div>
			</div>
		</div>

		{#if uploadResult}
			<div class:alert-success={!uploadResult.error} class:alert-error={uploadResult.error} class="alert mb-4 shadow-sm">
				{#if uploadResult.error}
					<span>{uploadResult.error}</span>
				{:else}
					<span><strong>{uploadResult.dataset?.name}</strong> uploaded — {uploadResult.rows} rows, {uploadResult.columns.length} columns</span>
				{/if}
				<button class="btn btn-ghost btn-sm" on:click={() => (uploadResult = null)} aria-label="Close notification">✕</button>
			</div>
		{/if}

		<div class="grid items-start gap-4 lg:grid-cols-[minmax(0,1fr)_20rem]">
			<section class="card overflow-hidden border border-base-300 bg-base-100 shadow-sm">
				<div class="flex items-center justify-between border-b border-base-300 p-5">
					<div>
						<p class="text-xs font-black tracking-[0.18em] text-base-content/50">LIBRARY</p>
						<h3 class="text-xl font-bold">All datasets</h3>
					</div>
					<span class="badge badge-primary">{datasets.length}</span>
				</div>

				{#if datasets.length === 0}
					<div class="flex min-h-72 flex-col items-center justify-center p-8 text-center">
						<div class="mb-4 grid size-14 place-items-center rounded-2xl bg-primary/10 text-primary">
							<svg class="size-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
								<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16v12H4zM8 6V4h8v2M8 10h8M8 14h5" />
							</svg>
						</div>
						<h4 class="font-bold">No datasets yet</h4>
						<p class="mt-1 text-sm text-base-content/60">Upload a CSV or create a dataset manually.</p>
					</div>
				{:else}
					<div class="overflow-x-auto">
						<table class="table">
							<thead>
								<tr>
									<th>Name</th>
									<th>Rows</th>
									<th class="text-right">Actions</th>
								</tr>
							</thead>
							<tbody>
								{#each datasets as dataset}
									<tr class="hover">
										<td>
											<div class="flex items-center gap-3">
												<div class="grid size-10 place-items-center rounded-xl bg-primary/10 text-primary">
													<svg class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
														<path stroke-linecap="round" stroke-linejoin="round" d="M7 3h7l4 4v14H7zM14 3v5h5M10 12h5M10 16h5" />
													</svg>
												</div>
												<strong>{dataset.name}</strong>
											</div>
										</td>
										<td><span class="badge badge-ghost">{dataset.rows?.toLocaleString() ?? 0}</span></td>
										<td class="text-right">
											<button
												class="btn btn-error btn-outline btn-sm"
												on:click={() => deleteDataset(dataset.id)}
												disabled={deletingId === dataset.id}
											>
												{deletingId === dataset.id ? 'Deleting...' : 'Delete'}
											</button>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{/if}
			</section>

			<aside class="card border border-base-300 bg-base-100 shadow-sm">
				<div class="border-b border-base-300 p-5">
					<p class="text-xs font-black tracking-[0.18em] text-base-content/50">NEW DATASET</p>
					<h3 class="text-xl font-bold">Create manually</h3>
				</div>

				<form class="space-y-3 p-5" on:submit|preventDefault={createDataset}>
					<label class="form-control">
						<span class="label-text mb-1 font-semibold">Dataset name</span>
						<input class="input input-bordered w-full" type="text" placeholder="e.g. Customers" bind:value={name} />
					</label>
					<label class="form-control">
						<span class="label-text mb-1 font-semibold">Number of rows</span>
						<input class="input input-bordered w-full" type="number" min="0" placeholder="0" bind:value={rows} />
					</label>
					<button class="btn btn-primary w-full" type="submit" disabled={!name.trim()}>Create dataset</button>
				</form>

				<div class="divider px-5 text-xs text-base-content/50">or</div>

				<label for="csv-file" class="m-5 mt-0 flex cursor-pointer items-center gap-3 rounded-xl border border-dashed border-primary/40 bg-primary/5 p-4 transition hover:bg-primary/10">
					<svg class="size-8 shrink-0 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 16V5m0 0L8 9m4-4l4 4M5 15v3a1 1 0 001 1h12a1 1 0 001-1v-3" />
					</svg>
					<span class="min-w-0">
						<strong class="block truncate text-sm">{selectedFile ? selectedFile.name : 'Choose a CSV file'}</strong>
						<span class="text-xs text-base-content/60">.csv files supported</span>
					</span>
				</label>
			</aside>
		</div>
	</section>
</main>
