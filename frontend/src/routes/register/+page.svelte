<script>
	import { enhance } from '$app/forms';

	const { form } = $props();
</script>

<section class="flex flex-col items-center h-screen justify-center bg-gray-50">
	<div>
		{#if form}
			{#if form.error}
				<p style="color: red;">Error: {form.error}</p>
			{:else if form.success}
				<p style="color: green;">{form.message}</p>
			{/if}
		{/if}
	</div>
	<form
		class="flex flex-col text-sm text-[#374151] bg-white shadow-lg shadow-gray-400 rounded-lg gap-4 p-4 m-4"
		method="POST"
		action="/auth?/register"
		use:enhance
	>
		<h1 class="text-[#1E3A8A] font-bold text-2xl">Create your account</h1>
		<label for="userName">
			Username
			<input
				placeholder="johndoe123"
				class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
				name="userName"
				type="userName"
			/>
		</label>
		<label for="email">
			Email
			<input
				placeholder="abc@yahoo.com"
				class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
				name="email"
				type="email"
			/>
		</label>
		<label for="fullName">
			Full Name
			<input
				placeholder="John Doe"
				class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
				name="fullName"
				type="fullName"
			/>
		</label>
		<label for="password">
			Password
			<input
				placeholder="At least 8 chracters"
				class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
				name="password"
				type="password"
			/>
		</label>
		<button
			class="bg-[#F97316] hover:bg-[#D86211] text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
			type="submit">Sign up</button
		>
		<p class="text-center text-xs">
			Already have an account? <a class="text-[#F97316] hover:text-[#D86211]" href="/login"
				>Log in</a
			>
		</p>
	</form>
</section>
