import React, { Component } from 'react';
import CanvasJSReact from '@canvasjs/react-charts';

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Graph1 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            unemploymentDataPoints: [],
            populationDataPoints: []
        };
    }

    componentDidMount() {
        this.fetchUnemploymentData();
        this.fetchPopulationData();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.selectedCountry !== this.props.selectedCountry || prevProps.yearRange !== this.props.yearRange) {
            this.fetchUnemploymentData();
            this.fetchPopulationData();
        }
    }

    fetchUnemploymentData = () => {
        const { yearRange } = this.props;
        const unemploymentData = [];
        const currentYear = new Date().getFullYear();
        const startYear = currentYear - yearRange + 1; // Początkowy rok na osi X
        const endYear = currentYear; // Końcowy rok na osi X
        for (let year = startYear; year <= endYear; year++) {
            const unemploymentRate = Math.random() * (10 - 5) + 5; // Random unemployment rate between 5% and 10%
            unemploymentData.push({ x: new Date(year, 0), y: unemploymentRate });
        }
        this.setState({ unemploymentDataPoints: unemploymentData });
    };

    fetchPopulationData = () => {
        const { yearRange } = this.props;
        const populationData = [];
        const currentYear = new Date().getFullYear();
        const startYear = currentYear - yearRange + 1; // Początkowy rok na osi X
        const endYear = currentYear; // Końcowy rok na osi X
        for (let year = startYear; year <= endYear; year++) {
            const population = Math.floor(Math.random() * (200000000 - 100000000) + 100000000); // Random population between 100 million and 200 million
            populationData.push({ x: new Date(year, 0), y: population });
        }
        this.setState({ populationDataPoints: populationData });
    };

    render() {
        const { unemploymentDataPoints, populationDataPoints } = this.state;

        const options1 = {
            title: {
                text: "Unemployment Rate"
            },
            axisX: {
                title: "Date Range",
                valueFormatString: "YYYY" // Formatowanie wartości osi X jako pełnych lat
            },
            axisY: {
                title: "Unemployment Rate (%)"
            },
            data: [{
                type: "line",
                dataPoints: unemploymentDataPoints
            }]
        };

        const options2 = {
            title: {
                text: "Population"
            },
            axisX: {
                title: "Date Range",
                valueFormatString: "YYYY" // Formatowanie wartości osi X jako pełnych lat
            },
            axisY: {
                title: "Population"
            },
            data: [{
                type: "line",
                dataPoints: populationDataPoints
            }]
        };

        return (
            <div className='container'>
                <CanvasJSChart options={options1} />
                <CanvasJSChart options={options2} />
            </div>
        );
    }    
}

export default Graph1;
