<script>
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	let { form } = $props();
	let showToast = $state(false);
	let toastMessage = $state('');
	let toastType = $state('success');

	$effect(() => {
		if (form?.success) {
			toastMessage = form.message;
			toastType = 'success';
			showToast = true;
			const timer = setTimeout(() => {
				showToast = false;
				goto(resolve('/login'));
			}, 2000);
			return () => clearTimeout(timer);
		} else if (form?.error) {
			toastMessage = form.error;
			toastType = 'error';
			showToast = true;
			const timer = setTimeout(() => {
				showToast = false;
			}, 3000);
			return () => clearTimeout(timer);
		}
	});
</script>

{#if showToast}
	<div
		class="fixed top-4 right-4 {toastType === 'success'
			? 'bg-green-500'
			: 'bg-red-500'} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-bounce"
	>
		{toastMessage}
	</div>
{/if}

<section class="flex flex-col items-center h-screen justify-center bg-gray-50">
	<form
		class="flex flex-col text-sm text-[#374151] bg-white shadow-lg shadow-gray-400 rounded-lg gap-4 p-4 m-4"
		method="POST"
		action="?/register"
		use:enhance
	>
		<h1 class="text-[#1E3A8A] font-bold text-2xl">Create your account</h1>
		<label for="userName">
			Username
			<input
				placeholder="johndoe123"
				class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
				name="userName"
				type="text"
				required
			/>
		</label>
		<label for="email">
			Email
			<input
				placeholder="abc@yahoo.com"
				class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
				name="email"
				type="email"
				required
			/>
		</label>
		<label for="fullName">
			Full Name
			<input
				placeholder="John Doe"
				class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
				name="fullName"
				type="text"
				required
			/>
		</label>
		<label for="password">
			Password
			<input
				placeholder="At least 8 characters"
				class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
				name="password"
				type="password"
				required
			/>
		</label>
		<button
			class="bg-[#F97316] hover:bg-[#D86211] text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
			type="submit">Sign up</button
		>
		<p class="text-center text-xs">
			Already have an account? <a
				class="text-[#F97316] hover:text-[#D86211]"
				href={resolve('/login')}>Log in</a
			>
		</p>
	</form>
</section>
