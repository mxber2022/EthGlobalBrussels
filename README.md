# EthGlobalBrussels
 
# Blind Feedback

Welcome to the Blind Feedback App! This application enables multiple parties to submit anonymous ratings and uses blind computation to determine the average rating. Additionally, it employs an AI model to analyze user sentiment. Essential information such as store ID and party names is securely stored on the Orbit blockchain for reference and perform data analysis.

## Features

- **Anonymous Rating Submission**: Users can submit ratings (0-9) anonymously.
- **Blind Computation**: Calculate the average rating using privacy-preserving Nada programs on the Nillion Network.
- **AI Sentiment Analysis**: Analyze user sentiments using an AI model.
- **Blockchain Storage**: Store essential information securely on the Orbit blockchain.

## Workflow

1. **Rating Submission**: Users submit their ratings (0-9) anonymously through the app.
2. **Blind Computation**: The collected ratings are sent to the Nillion Network, where a Nada program calculates the average rating.
4. **Blockchain Storage**: Store ID and party names are recorded on the Orbit blockchain.
3. **Sentiment Analysis**: User feedback is analyzed using an AI model to determine sentiment.


## Arbitrum orbit chain details
0x629Fb566FD8f318d6c5E2559f55C80Dbb73F92E3 - smartcontract
http://localhost:8449/ - rpc

## Rating Scale

- **0**: Terrible
- **1**: Poor
- **2**: Bad
- **3**: Mediocre
- **4**: Fair
- **5**: Average
- **6**: Good
- **7**: Very Good
- **8**: Excellent
- **9**: Fire

## Acknowledgements
- Nillion for the secure computation network
- Orbit for the blockchain technology
- Hugging Face for the AI sentiment analysis models

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/)
- [Nillion SDK](https://nillion.network/sdk)
- [Orbit Blockchain SDK](https://orbit.network/sdk)
- [Python](https://www.python.org/) (for AI model)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/anonymous-survey-sentiment-app.git
   cd anonymous-survey-sentiment-app
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your configurations:

   ```env
   NILLION_API_KEY=your_nillion_api_key
   ORBIT_API_KEY=your_orbit_api_key
   AI_MODEL_PATH=path_to_your_ai_model
   ```

4. **Run the Application**

   ```bash
   npm start
   ```

### Usage

1. **Submit Ratings**

   Users can submit their ratings (0-9).

2. **View Average Rating and Sentiment Analysis**

   The app calculates the average rating using blind computation and displays the results along with sentiment analysis insights.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Nillion Network](https://nillion.network/)
- [Orbit Blockchain](https://orbit.network/)
- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)

---

Feel free to open an issue or submit a pull request if you have any questions or improvements. Thank you for using the Anonymous Survey and AI Sentiment App!