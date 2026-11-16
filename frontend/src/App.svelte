<script>

	let datasets = [];

	let name = "";
	let rows = 0;

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





