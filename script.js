const MY_GITHUB_TOKEN = 'your_github_token_here';  // Replace with your actual token

document.getElementById('youtube-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const youtubeLink = document.getElementById('youtube-link').value;
    const blogOutput = document.getElementById('blog-output');

    blogOutput.innerHTML = '<p>Generating blog... Please wait.</p>';

    try {
        // Call GitHub Actions workflow
        const response = await fetch('https://api.github.com/repos/<your-username>/<your-repo>/dispatches', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${MY_GITHUB_TOKEN}`,
            },
            body: JSON.stringify({
                event_type: 'generate-blog',
                client_payload: {
                    youtubeLink: youtubeLink,
                },
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to trigger blog generation');
        }

        // Wait for the workflow to complete and fetch the result
        const data = await response.json();
        blogOutput.innerHTML = `<div>${data.blogContent}</div>`;
    } catch (error) {
        blogOutput.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});