<script>
	import './layout.css';
	// import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" />
</svelte:head>

{@render children()}
