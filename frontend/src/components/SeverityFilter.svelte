<script>
    import { vulnerabilities } from "../lib/vulnerabilityStore.js";
    import { derived, writable } from "svelte/store";
    export let vulnerabilities;
    
    let selectedSeverity = writable("");

    const filteredVulnerabilities = derived(
        [vulnerabilities, selectedSeverity],
        ([$vulnerabilities, $selectedSeverity]) => {
            if (!$selectedSeverity) return $vulnerabilities;
            return $vulnerabilities.filter(v => v.severity === $selectedSeverity);
        }
    );
</script>

<div class="filter-container">
    <h3>Filter Vulnerabilities by Severity</h3>
    <select bind:value={$selectedSeverity} class="filter-select">
        <option value="">All</option>
        <option value="critical">Critical</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
        <option value="unknown">Unknown</option>
    </select>

    <table class="vulnerability-table">
        <thead>
            <tr>
                <th>Description</th>
                <th>Function</th>
                <th>PC</th>
                <th>Line</th>
                <th>Severity</th>
            </tr>
        </thead>
        <tbody>
            {#if $filteredVulnerabilities.length > 0}
                {#each $filteredVulnerabilities as vuln}
                    <tr>
                        <td>{vuln.description}</td>
                        <td>{vuln.function || 'N/A'}</td>
                        <td>{vuln.pc || 'N/A'}</td>
                        <td>{vuln.line || 'N/A'}</td>
                        <td class="severity {vuln.severity}">{vuln.severity}</td>
                    </tr>
                {/each}
            {:else}
                <tr>
                    <td colspan="5">No vulnerabilities found for the selected severity.</td>
                </tr>
            {/if}
        </tbody>
    </table>
</div>

<style>
.filter-container {
    margin-top: 20px;
    padding: 16px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filter-select {
    width: 100%;
    max-width: 200px;
    margin-bottom: 12px;
    padding: 6px;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    background-color: #f8fafc;
}

.vulnerability-table {
    width: 100%;
    border-collapse: collapse;
}

.vulnerability-table th, .vulnerability-table td {
    padding: 10px;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
}

.severity {
    text-transform: capitalize;
    font-weight: bold;
}

.severity.critical { color: #ef4444; }
.severity.high { color: #f97316; }
.severity.medium { color: #f59e0b; }
.severity.low { color: #84cc16; }
.severity.unknown { color: #64748b; }
</style>
