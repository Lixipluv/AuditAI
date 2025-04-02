<script>
    export let reportData = [];
  
    const severityColor = (impact) => {
      switch (impact.toLowerCase()) {
        case "critical":
          return "bg-red-600";
        case "high":
          return "bg-orange-500";
        case "medium":
          return "bg-yellow-400";
        case "low":
          return "bg-green-500";
        default:
          return "bg-gray-400";
      }
    };
  </script>
  
  <div class="space-y-4 mt-8">
    {#if reportData.length === 0}
      <p class="text-gray-500 italic">Nenhum dado de análise encontrado.</p>
    {:else}
      {#each reportData as item, index}
        <div class="bg-white dark:bg-gray-800 shadow-md rounded-2xl p-4 border border-gray-200 dark:border-gray-700 transition-all hover:shadow-lg">
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">
              {item.check}
            </h3>
            <span class={`text-xs px-2 py-1 rounded-full text-white ${severityColor(item.impact)}`}>
              {item.impact}
            </span>
          </div>
  
          <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
            {item.description}
          </p>
  
          <div class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            <strong>Confiança:</strong> {item.confidence}
          </div>
        </div>
      {/each}
    {/if}
  </div>
  