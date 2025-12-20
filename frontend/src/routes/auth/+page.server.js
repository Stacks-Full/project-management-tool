/** @satisfies {import('./$types').Actions} */
export const actions = {
	register: async (event) => {
		const formData = await event.request.formData();
		const email = formData.get('email');
		const password = formData.get('password');
		const userName = formData.get('userName');
		const fullName = formData.get('fullName');

		console.log(email, password, userName, fullName);

		return;
	}
};
