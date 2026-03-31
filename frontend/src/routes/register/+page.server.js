import { fail } from '@sveltejs/kit';

/** @satisfies {import('./$types').Actions} */
export const actions = {
	register: async (event) => {
		const formData = await event.request.formData();
		const email = formData.get('email');
		const password = formData.get('password');
		const username = formData.get('userName');
		const full_name = formData.get('fullName');

		if (!email || !password || !username || !full_name) {
			return fail(400, { error: 'All fields are required' });
		}

		try {
			// Try connecting to 'backend' (docker) first, fallback to '0.0.0.0' or 'localhost'
			// In a real app, this should be an environment variable
			const backendUrl = 'http://backend:8000/api/v1/auth/register';

			const response = await fetch(backendUrl, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					full_name,
					email,
					username,
					password
				})
			});

			const result = await response.json();

			if (!response.ok) {
				return fail(response.status, {
					error: result.detail || 'Registration failed'
				});
			}

			return {
				success: true,
				message: 'Registration successful! Redirecting to login...'
			};
		} catch (error) {
			console.error('Registration error:', error);
			// Fallback for non-docker environment
			try {
				const fallbackUrl = 'http://localhost:8000/api/v1/auth/register';
				const response = await fetch(fallbackUrl, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						full_name,
						email,
						username,
						password
					})
				});
				const result = await response.json();
				if (!response.ok) {
					return fail(response.status, {
						error: result.detail || 'Registration failed'
					});
				}
				return {
					success: true,
					message: 'Registration successful! Redirecting to login...'
				};
			} catch (fallbackError) {
				console.error('Fallback registration error:', fallbackError);
				return fail(500, { error: 'Could not connect to the server' });
			}
		}
	}
};
