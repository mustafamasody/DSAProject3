
const config = {
  content: [
	"./src/**/*.{js,jsx,ts,tsx}",
  ],
	theme: {
	  extend: {
		gridTemplateColumns: {
			// Simple 31 column grid
			'31': 'repeat(31, minmax(0, 1fr))',
	
			// Complex site-specific column configuration
			'footer': '200px minmax(900px, 1fr) 100px',
		},
		gridColumn: {
			'span-2.5': 'span 2.5 / span 2.5',
		},
		padding: {
			'safe-bottom': 'env(safe-area-inset-bottom)',
		},
		keyframes: {
			wiggle: {
				"0%, 100%": { transform: "rotate(-3deg)" },
				"50%": { transform: "rotate(3deg)" }
			  }
		  },
		  animation: {
			wiggle: "wiggle 200ms ease-in-out"
		  },
		  
		boxShadow: {
			'3xl': '0 35px 60px -15px rgba(0, 0, 0, 0.3)',
		  },
		screens: {
			mobile: "320px",
			tablet: "480px",
			laptop: "770px",
			desktop: "1024px",
			desktop2: "1280px",
			xl: "1440px",
			mmxl: "1500px",
			prehalfxl: "1660px",
			halfxl: "1600px",
			halfxlactual: "1805px",
			threequarterxl: "1920px",
			threequarterxl2: "1960px",
			threequarterxl3: "2000px",
			threefivequarterxl: "2044px",
			halfxxl: "2148px",
			xxl: "2412px",
			threexl: "2560px",
			threexl2: "2700px",
			halfhalf: "1078px",

		},
		colors: {
			black: '#000', // Define a custom black color if necessary
		  primaryold: '#2563eb',
		  secondaryold: '#172554',
		  light: '#e6e6e6',
		  dark: '#363636',
		  background: "#ffffff", // light grey
		  backgroundDark: "#0a0a0a", // dark grey
		  foreground: "#f4f6f8", // white
		  foregroundDark: "#191919", // black
		  neutralLight: "#efefef",

		  v2background: "#000d12",
		  v2hover: "#001117",

		  primary: "#02102e",
		  primaryv2: "#031640",
		  secondary: "#041b4d",
		  hover: "#03205e",
		  hoverlighter: "#042b7f",
		  headerdark: "#020d24",
		  lighterblue: "#2062f1",
		  navbar: "#031845",


			primarynewdark: "#131313",
			primaryv2newdark: "#171717",
			secondarynewdark: "#27272a",
			hovernewdark: "#404040",
			hoverlighternewdark: "#525252",
			headerdarknewdark: "#000000",
			lighterbluenewdark: "#2062f1",
			navbarnewdark: "#171717",
		}
	  },
	},
	plugins: [],
};
export default config;
