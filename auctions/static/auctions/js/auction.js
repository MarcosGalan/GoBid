function getExistingBets() {
    if (!document.getElementById('bets'))
        return [{username: '', amount: 0}]

    return Array.from(document.getElementById('bets').querySelectorAll('li')).map(bet => ({
        username: bet.querySelector('#username').textContent.trim(),
        amount: bet.querySelector('#amount').textContent.trim()
    }));
}

function getHighestBet() {
    const existingBets = getExistingBets();
    return Math.max(...existingBets.map(bet => parseFloat(bet.amount)));
}


const betsDelay = 2000;

const auctionFetchInterval = setInterval(() => {
    const auctionId = getAuctionId();
    if (!auctionId) {
        console.warn('Auction ID not found. Skipping fetching bets.');
        return;
    }

    // Get updated bets
    fetch(`/auctions/fetch/auction/${getAuctionId()}/`)
        .then(response => response.json())
        .then(data => {
            if (data === undefined || data.length === 0) {
                clearInterval(auctionFetchInterval)
                return
            }

            // Extract relevant information
            const newBets = data.map(item => ({
                username: item.user.username,
                amount: item.bet_amount,
            }));


            // Find the maximum amount in the existing bets
            const maxAmount = getHighestBet();

            // Filter new bets based on the maximum amount
            const filteredBets = newBets.filter(bet => parseFloat(bet.amount) > maxAmount);


            // Update the DOM with the new bets
            const betsList = document.getElementById('bets');
            filteredBets.forEach(newBet => {
                const li = document.createElement('li');
                li.innerHTML = `
                <a href="#">
                    <div id="username" style="display: inline-block">${newBet.username}</div>
                </a> raises the bet to 
                <span>
                    <div id="amount" style="display: inline-block">${newBet.amount}</div>
                </span>`;

                let lastLi = betsList.lastElementChild;

                if (lastLi) {
                    betsList.removeChild(lastLi);
                } else {
                    console.log("The list is empty.");
                }

                betsList.insertBefore(li, betsList.firstChild); // Add to the top of the list

                setTimeout(() => li.classList.add('appear'), 100)
            });
        })
        .catch(error => console.error('Error fetching bets:', error));
}, betsDelay)


function getAuctionId() {
    // Get the current URL path
    const currentPath = window.location.pathname;

    const regex = /\/auctions\/auction\/(\d+)\/$/;

    const match = currentPath.match(regex);
    const auctionId = match ? match[1] : null;

    return auctionId;
}


function validateNewBet() {
    const currentBet = parseInt(document.querySelector('.bet-input').value, 10);
    const highestBet = getHighestBet(); // Replace this with the function to get the highest bet amount

    if (currentBet <= highestBet) {
        // Display SweetAlert confirmation
        Swal.fire({
            icon: 'warning',
            title: 'Invalid Bet',
            text: 'The bet amount must be higher than the current highest bet.',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'OK'
        });

        return false;
    }

    return true;
}

function increaseBet(amount) {
    const inputElement = document.querySelector('.bet-input');
    const currentBet = parseInt(inputElement.value, 10);
    inputElement.value = currentBet + amount;
}

document.getElementById('betForm').addEventListener('submit', function (event) {
    // Execute validateNewBet() before submitting the bet
    if (!validateNewBet())
        event.preventDefault();
});


// Countdown
const endDateString = document.getElementById('countdown').dataset.endDate;
const endDate = Date.parse(endDateString);

function countdown() {
    // Get the current date and time
    const now = new Date().getTime();

    // Calculate the time remaining
    const timeRemaining = endDate - now;

    if (timeRemaining <= 0) {
        // If the countdown has expired, display a message
        clearInterval(countdownInterval);
        document.getElementById('countdown').innerHTML = 'Auction has ended.';

        Swal.fire({
            icon: 'success',
            title: 'Auction has ended.',
            text: 'The auction has ended. You can no longer place bets.\nThank you for participating!',
            confirmButtonColor: '#d66a30',
            confirmButtonText: 'OK'
        });

        // Disable the bet button
        document.getElementById('betButton').disabled = true;


    } else {
        // Calculate days, hours, minutes, and seconds
        const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

        // Display the countdown
        document.getElementById('countdown').innerHTML = `Ends in ${days}d ${hours}h ${minutes}m ${seconds}s`;
    }
}

const countdownInterval = setInterval(() => countdown(), 1000);
countdown();


// Set the initial bet amount as the highest bet
document.querySelector('.bet-input').value = getHighestBet();