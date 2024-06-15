const app = Vue.createApp({
    data() {
        return {
            scrapers: {},
            profiles: {}
        };
    },
    delimiters: ['[[', ']]'],
    created() {
        this.connectSocket();
    },
    methods: {
        connectSocket() {
            const socket = io('http://localhost:5000'); // Explicitly specify the WebSocket URL
            
            socket.on('connect', () => {
                console.log('Connected to WebSocket');
            });

            socket.on('scraper_status', (data) => {
                this.scrapers = data;
                console.log('Scraper Status:', data);
            });

            socket.on('profiles_status', (data) => {
                this.profiles = data;
                console.log('Profiles Status:', data);
            });

            socket.on('disconnect', () => {
                console.log('WebSocket disconnected. Reconnecting...');
                setTimeout(this.connectSocket, 1000);
            });
        },
        getScrapersByProfile(profileName) {
            return Object.values(this.scrapers).filter(scraper => scraper.profile_name === profileName);
        },
        formatDate(dateString) {
            const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        },
        
        formatDuration(durationString) {
            if (durationString) {
                return durationString.split('.')[0]; // Remove milliseconds from duration
            }
            return ''; // Return an empty string if durationString is undefined
        }
    }
});

app.mount('#app');
