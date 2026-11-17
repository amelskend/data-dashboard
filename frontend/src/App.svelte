<script>

	let datasets = [];

	let name = "";
	let rows = 0;
	let uploadResult = null;

	async function loadDatasets() {

		const response = await fetch(
			"http://localhost:8000/datasets"
		);

		datasets = await response.json();
	}

	async function createDataset() {

		await fetch(
			"http://localhost:8000/datasets",
			{
				method: "POST",

				headers: {
					"Content-Type": "application/json"
				},

				body: JSON.stringify({
					name,
					rows
				})
			}
		);
    

		await loadDatasets();

		name = "";
		rows = 0;
	}
  async function deleteDataset(id) {

	  await fetch(
	  	`http://localhost:8000/datasets/${id}`,
	  	{
	  		method: "DELETE"
	  	}
	  );

	  await loadDatasets();
  }
	loadDatasets();
  async function uploadCsv(event) {

    const formData = new FormData();

    formData.append(
        "file",
        event.target.files[0]
    );

    const response = await fetch(
      "http://localhost:8000/upload",
      {
        method: "POST",
        body: formData
      }
    );

    const result = await response.json();
    console.log(result);
	uploadResult = result;
  }

</script>

<h1 class="text-5xl font-bold text-blue-400">
  Datasets
</h1>

<ul>

	{#each datasets as dataset}
		<li>{dataset.name}</li>
    <p>{dataset.rows}</p>
    <button
    class="btn btn-error"
    on:click={() => deleteDataset(dataset.id)}
      >
    Delete
    </button>

	{/each}

</ul>
<input
	type="text"
	placeholder="Dataset name"
	bind:value={name}
/>

<input
	type="number"
	placeholder="Rows"
	bind:value={rows}
/>

<button
 class="btn btn-primary"
 on:click={createDataset}
>
 Add Dataset
</button>

<div class="flex items-center gap-2">
  <label for="csv-file" class="btn btn-secondary">
    Upload CSV
  </label>
  <input
    id="csv-file"
    class="hidden"
    type="file"
    accept=".csv"
    on:change={uploadCsv}
  />
</div>

{#if uploadResult}

<div class="alert alert-success">

 Rows: {uploadResult.rows}

 Columns:

 {uploadResult.columns.join(", ")}

</div>

{/if}