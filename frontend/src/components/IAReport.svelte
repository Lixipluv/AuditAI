<script>
    export let htmlContent = "";
  </script>
  
  <div class="prose max-w-full dark:prose-invert prose-h2:text-blue-600 prose-h3:text-gray-800 prose-p:leading-7 prose-strong:text-black" bind:this={container}>
    {@html htmlContent}
  </div>
  