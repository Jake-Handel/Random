// Game state
let cookies = 0;
let totalCookiesBaked = 0;
let cookiesPerSecond = 0;
let goldenCookiesClicked = 0;
let gameStartTime = Date.now();
let lastUpdateTime = Date.now();

// Upgrade configurations
const upgrades = {
    cursor: {
        name: 'Cursor',
        baseCost: 15,
        cost: 15,
        production: 0.1,
        count: 0,
        description: 'Autoclicks every 10 seconds',
        icon: 'fa-mouse-pointer',
        unlocked: true
    },
    grandma: {
        name: 'Grandma',
        baseCost: 100,
        cost: 100,
        production: 1,
        count: 0,
        description: 'A nice grandma to bake more cookies',
        icon: 'fa-user',
        unlockAt: 10
    },
    farm: {
        name: 'Farm',
        baseCost: 1100,
        cost: 1100,
        production: 8,
        count: 0,
        description: 'Grows cookie plants from cookie seeds',
        icon: 'fa-tractor',
        unlockAt: 50
    },
    factory: {
        name: 'Factory',
        baseCost: 12000,
        cost: 12000,
        production: 47,
        count: 0,
        description: 'Produces large quantities of cookies',
        icon: 'fa-industry',
        unlockAt: 500
    },
    mine: {
        name: 'Mine',
        baseCost: 130000,
        cost: 130000,
        production: 260,
        count: 0,
        description: 'Mines out cookie dough and chocolate chips',
        icon: 'fa-mountain',
        unlockAt: 5000
    },
    shipment: {
        name: 'Shipment',
        baseCost: 1400000,
        cost: 1400000,
        production: 1400,
        count: 0,
        description: 'Brings in fresh cookies from the cookie planet',
        icon: 'fa-rocket',
        unlockAt: 50000
    }
};

// Achievements configuration
const achievements = [
    { id: 'first_click', name: 'First Click', description: 'Bake your first cookie', condition: () => totalCookiesBaked >= 1, icon: 'fa-cookie-bite', bonus: 0.1 },
    { id: 'hundred', name: 'Hundred', description: 'Bake 100 cookies', condition: () => totalCookiesBaked >= 100, icon: 'fa-hashtag', bonus: 0.2 },
    { id: 'thousand', name: 'Thousand', description: 'Bake 1,000 cookies', condition: () => totalCookiesBaked >= 1000, icon: 'fa-th', bonus: 0.5 },
    { id: 'million', name: 'Millionaire', description: 'Bake 1,000,000 cookies', condition: () => totalCookiesBaked >= 1000000, icon: 'fa-money-bill-wave', bonus: 2 },
    { id: 'first_upgrade', name: 'First Upgrade', description: 'Purchase your first upgrade', condition: () => Object.values(upgrades).some(u => u.count > 0), icon: 'fa-arrow-up', bonus: 0.1 },
    { id: 'golden_cookie', name: 'Golden Cookie!', description: 'Click a golden cookie', condition: () => goldenCookiesClicked > 0, icon: 'fa-star', bonus: 0.5 },
    { id: 'speed_baker', name: 'Speed Baker', description: 'Reach 100 cookies per second', condition: () => cookiesPerSecond >= 100, icon: 'fa-bolt', bonus: 1 },
    { id: 'cookie_tycoon', name: 'Cookie Tycoon', description: 'Own 100 buildings', condition: () => Object.values(upgrades).reduce((sum, u) => sum + u.count, 0) >= 100, icon: 'fa-crown', bonus: 2 }
];

// DOM elements
const cookieElement = document.getElementById('cookie');
const cookieCountElement = document.getElementById('cookie-count');
const cookiesPerSecondElement = document.getElementById('cookies-per-second');
const totalCookiesElement = document.getElementById('total-cookies');
const achievementCountElement = document.getElementById('achievement-count');
const achievementsContainer = document.getElementById('achievements-container');
const notificationElement = document.getElementById('notification');
const goldenCookieElement = document.getElementById('golden-cookie');

// Game initialization
function init() {
    loadGame();
    setupEventListeners();
    createUpgradeElements();
    createAchievementElements();
    updateDisplay();
    
    // Start game loop
    setInterval(update, 50); // 20 updates per second for smooth animations
    setInterval(spawnGoldenCookie, 30000); // Spawn golden cookie every 30 seconds
}

// Set up event listeners
function setupEventListeners() {
    // Cookie click
    cookieElement.addEventListener('click', () => {
        addCookies(1);
        createClickEffect(event);
    });
    
    // Golden cookie click
    goldenCookieElement.addEventListener('click', () => {
        goldenCookieClick();
    });
    
    // Save game when page is closed
    window.addEventListener('beforeunload', saveGame);
}

// Create upgrade elements
function createUpgradeElements() {
    const upgradesGrid = document.querySelector('.upgrades-grid');
    
    Object.entries(upgrades).forEach(([id, upgrade]) => {
        if (upgrade.unlockAt) return; // Skip if not unlocked by default
        
        const element = document.createElement('div');
        element.className = 'upgrade';
        element.id = id;
        element.innerHTML = `
            <div class="upgrade-icon"><i class="fas ${upgrade.icon}"></i></div>
            <div class="upgrade-info">
                <h3>${upgrade.name}</h3>
                <p>${upgrade.description}</p>
                <div class="upgrade-stats">
                    <span class="upgrade-count">0</span> owned
                    <span class="upgrade-cps">+${upgrade.production} each</span>
                </div>
            </div>
            <button class="upgrade-btn" onclick="buyUpgrade('${id}')">
                <span class="cost">${formatNumber(upgrade.cost)}</span> cookies
            </button>
        `;
        upgradesGrid.appendChild(element);
    });
}

// Create achievement elements
function createAchievementElements() {
    achievementsContainer.innerHTML = '';
    
    achievements.forEach(achievement => {
        const element = document.createElement('div');
        element.className = `achievement ${achievement.condition() ? 'unlocked' : 'locked'}`;
        element.id = `achievement-${achievement.id}`;
        element.innerHTML = `
            <div class="achievement-icon">
                <i class="fas ${achievement.icon}"></i>
            </div>
            <div class="achievement-info">
                <h4>${achievement.name}</h4>
                <p>${achievement.description}</p>
            </div>
            <div class="achievement-status">
                ${achievement.condition() ? '✓' : '🔒'}
            </div>
        `;
        achievementsContainer.appendChild(element);
    });
}

// Main game loop
function update() {
    const now = Date.now();
    const deltaTime = (now - lastUpdateTime) / 1000; // Convert to seconds
    lastUpdateTime = now;
    
    // Update cookies based on production
    if (cookiesPerSecond > 0) {
        const cookiesToAdd = cookiesPerSecond * deltaTime;
        addCookies(cookiesToAdd, false);
    }
    
    // Update stats
    updateStats();
    
    // Check for unlocked achievements
    checkAchievements();
    
    // Update display
    updateDisplay();
}

// Add cookies to the total
function addCookies(amount, fromClick = true) {
    if (fromClick) {
        totalCookiesBaked += amount;
    }
    cookies += amount;
}

// Update the display
function updateDisplay() {
    // Update cookie count
    cookieCountElement.textContent = `${formatNumber(Math.floor(cookies))} Cookies`;
    totalCookiesElement.textContent = formatNumber(Math.floor(totalCookiesBaked));
    
    // Update cookies per second
    cookiesPerSecondElement.textContent = `${formatNumber(cookiesPerSecond.toFixed(1))}/sec`;
    
    // Update upgrade buttons
    Object.entries(upgrades).forEach(([id, upgrade]) => {
        const element = document.getElementById(id);
        if (!element) return;
        
        const costElement = element.querySelector('.cost');
        const countElement = element.querySelector('.upgrade-count');
        const button = element.querySelector('button');
        
        if (costElement) costElement.textContent = formatNumber(Math.floor(upgrade.cost));
        if (countElement) countElement.textContent = upgrade.count;
        
        // Check if upgrade should be unlocked
        if (upgrade.unlockAt && totalCookiesBaked >= upgrade.unlockAt && !upgrade.unlocked) {
            upgrade.unlocked = true;
            createUpgradeElement(upgrade);
        }
        
        // Update button state
        if (button) {
            button.disabled = cookies < upgrade.cost || !upgrade.unlocked;
            button.style.opacity = upgrade.unlocked ? '1' : '0.6';
        }
    });
}

// Update game stats
function updateStats() {
    // Calculate CPS
    let cps = 0;
    Object.values(upgrades).forEach(upgrade => {
        cps += upgrade.count * upgrade.production;
    });
    cookiesPerSecond = cps;
    
    // Update time played
    const timePlayed = Math.floor((Date.now() - gameStartTime) / 1000);
    document.getElementById('time-played').textContent = formatTime(timePlayed);
    
    // Update golden cookies clicked
    document.getElementById('golden-cookies-clicked').textContent = goldenCookiesClicked;
    document.getElementById('total-cookies-baked').textContent = formatNumber(Math.floor(totalCookiesBaked));
}

// Buy an upgrade
function buyUpgrade(upgradeId) {
    const upgrade = upgrades[upgradeId];
    if (!upgrade || cookies < upgrade.cost) return;
    
    cookies -= upgrade.cost;
    upgrade.count++;
    upgrade.cost = Math.floor(upgrade.baseCost * Math.pow(1.15, upgrade.count));
    
    // Visual feedback
    const element = document.getElementById(upgradeId);
    if (element) {
        element.classList.add('purchased');
        setTimeout(() => element.classList.remove('purchased'), 200);
    }
    
    showNotification(`Purchased ${upgrade.name}!`);
    saveGame();
}

// Spawn a golden cookie
function spawnGoldenCookie() {
    if (Math.random() > 0.3) return; // 30% chance to spawn
    
    const viewportWidth = window.innerWidth - 100;
    const viewportHeight = window.innerHeight - 100;
    
    const x = Math.max(50, Math.floor(Math.random() * viewportWidth));
    const y = Math.max(50, Math.floor(Math.random() * viewportHeight));
    
    goldenCookieElement.style.left = `${x}px`;
    goldenCookieElement.style.top = `${y}px`;
    goldenCookieElement.classList.add('visible');
    
    // Auto hide after 10 seconds
    setTimeout(() => {
        goldenCookieElement.classList.remove('visible');
    }, 10000);
}

// Handle golden cookie click
function goldenCookieClick() {
    const bonus = Math.floor(cookiesPerSecond * (10 + Math.random() * 20)); // 10-30x CPS
    addCookies(bonus);
    goldenCookiesClicked++;
    goldenCookieElement.classList.remove('visible');
    
    showNotification(`Golden Cookie! +${formatNumber(bonus)} cookies!`, 'warning');
    
    // Visual effect
    const effect = document.createElement('div');
    effect.className = 'golden-effect';
    effect.textContent = `+${formatNumber(bonus)}!`;
    effect.style.left = `${parseInt(goldenCookieElement.style.left) + 30}px`;
    effect.style.top = `${parseInt(goldenCookieElement.style.top) - 20}px`;
    document.body.appendChild(effect);
    
    setTimeout(() => {
        effect.remove();
    }, 2000);
    
    saveGame();
}

// Create click effect
function createClickEffect(event) {
    const effect = document.createElement('div');
    effect.className = 'click-effect';
    effect.style.left = `${event.clientX}px`;
    effect.style.top = `${event.clientY}px`;
    document.body.appendChild(effect);
    
    // Animate
    setTimeout(() => {
        effect.style.transform = 'translate(-50%, -50%) scale(3)';
        effect.style.opacity = '0';
    }, 10);
    
    // Remove after animation
    setTimeout(() => {
        effect.remove();
    }, 500);
}

// Show notification
function showNotification(message, type = 'success') {
    notificationElement.textContent = message;
    notificationElement.className = `notification show ${type}`;
    
    setTimeout(() => {
        notificationElement.classList.remove('show');
    }, 3000);
}

// Check for unlocked achievements
function checkAchievements() {
    let unlockedCount = 0;
    
    achievements.forEach(achievement => {
        const element = document.getElementById(`achievement-${achievement.id}`);
        if (!element) return;
        
        const isUnlocked = achievement.condition();
        if (isUnlocked && !element.classList.contains('unlocked')) {
            element.classList.add('unlocked');
            showNotification(`Achievement Unlocked: ${achievement.name}!`, 'warning');
            
            // Apply bonus
            if (achievement.bonus) {
                const bonus = 1 + (achievement.bonus / 100);
                Object.values(upgrades).forEach(upgrade => {
                    upgrade.production *= bonus;
                });
            }
        }
        
        if (isUnlocked) unlockedCount++;
    });
    
    // Update achievement count
    achievementCountElement.textContent = unlockedCount;
}

// Save game state
function saveGame() {
    const gameState = {
        cookies,
        totalCookiesBaked,
        goldenCookiesClicked,
        gameStartTime,
        upgrades: {},
        version: '1.1'
    };
    
    // Save upgrade states
    Object.entries(upgrades).forEach(([id, upgrade]) => {
        gameState.upgrades[id] = {
            count: upgrade.count,
            cost: upgrade.cost
        };
    });
    
    localStorage.setItem('cookieClickerSave', JSON.stringify(gameState));
}

// Load game state
function loadGame() {
    const savedGame = localStorage.getItem('cookieClickerSave');
    if (!savedGame) return;
    
    try {
        const gameState = JSON.parse(savedGame);
        
        // Load basic stats
        cookies = gameState.cookies || 0;
        totalCookiesBaked = gameState.totalCookiesBaked || 0;
        goldenCookiesClicked = gameState.goldenCookiesClicked || 0;
        
        // Adjust game start time for offline progress
        if (gameState.lastSave) {
            const offlineTime = (Date.now() - gameState.lastSave) / 1000; // in seconds
            if (offlineTime > 0) {
                const offlineCookies = offlineTime * cookiesPerSecond;
                if (offlineCookies > 0) {
                    addCookies(offlineCookies, false);
                    showNotification(`Welcome back! You earned ${formatNumber(Math.floor(offlineCookies))} cookies while you were away!`, 'warning');
                }
            }
        }
        
        // Load upgrades
        if (gameState.upgrades) {
            Object.entries(gameState.upgrades).forEach(([id, upgradeData]) => {
                if (upgrades[id]) {
                    upgrades[id].count = upgradeData.count || 0;
                    upgrades[id].cost = upgradeData.cost || upgrades[id].baseCost;
                    
                    // Unlock if count > 0
                    if (upgrades[id].count > 0) {
                        upgrades[id].unlocked = true;
                    }
                }
            });
        }
        
    } catch (e) {
        console.error('Failed to load saved game:', e);
    }
}

// Helper functions
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return Math.floor(num).toLocaleString();
}

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    return [
        hours > 0 ? hours + 'h' : '',
        minutes > 0 ? minutes + 'm' : '',
        secs + 's'
    ].filter(Boolean).join(' ');
}

// Start the game
window.onload = init;
