<script>
  import { onMount } from 'svelte';
  import { vulnerabilities, updateVulnerabilities } from '../../lib/vulnerabilityStore.js';
  import VulnerabilityChart from '../../components/VulnerabilityChart.svelte';
  import SeverityFilter from '../../components/SeverityFilter.svelte';

  let socket;

  onMount(() => {
    socket = new WebSocket('ws://localhost:8000/ws/dashboard');

    socket.onopen = () => {
      console.log('✅ WebSocket conectado ao Dashboard');
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      // Atualize diretamente as vulnerabilidades
      updateVulnerabilities(data.severity_counts);

      console.log('📦 Dados recebidos:', data);
    };

    socket.onerror = (error) => {
      console.error('⚠️ Erro no WebSocket:', error);
    };

    socket.onclose = () => {
      console.log('🚫 WebSocket fechado, reconectando em 5 segundos...');
      setTimeout(() => onMount(), 5000);
    };

    return () => socket.close();
  });
</script>

<SeverityFilter {vulnerabilities} />
<VulnerabilityChart {vulnerabilities} />
