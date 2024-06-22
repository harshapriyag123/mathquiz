document.addEventListener('DOMContentLoaded', async () => {
    const leaderboardBody = document.getElementById('leaderboard-body');

    try {
        const response = await fetch('/get_leaderboard');
        const users = await response.json();

        users.forEach((user, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${user.email}</td>
                <td>${user.score}</td>
            `;
            leaderboardBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching leaderboard data:', error);
    }
});
