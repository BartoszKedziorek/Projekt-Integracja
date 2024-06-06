import React, { Component } from 'react';
import Graph1 from './Graph1'; // Adjust the import path as necessary
import Graph3 from './Graph3';
import Graph4 from './Graph4';
import axios from 'axios';
import './GraphComparison.css'; // Import the CSS file for styling

class GraphComparison extends Component {
    constructor(props) {
        super(props);
        this.state = {
            countries: [],
            selectedCountry: '',
            yearRange: 5,
            isLoggedIn: !!localStorage.getItem('token') // Check if the user is logged in
        };
    }

    componentDidMount() {
        this.fetchCountries();
    }

    fetchCountries = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8001/api/country');
            const countries = response.data;
            if (countries.length > 0) {
                this.setState({ countries, selectedCountry: countries[1].code });
            } else {
                console.warn('No countries found in response');
            }
        } catch (error) {
            console.error('Error fetching countries', error);
        }
    };

    handleCountryChange = (e) => {
        this.setState({ selectedCountry: e.target.value });
    };

    handleYearRangeChange = (e) => {
        this.setState({ yearRange: parseInt(e.target.value, 10) });
    };

    handleLogout = () => {
        localStorage.removeItem('token');
        this.setState({ isLoggedIn: false });
    };

    render() {
        const { countries, selectedCountry, yearRange } = this.state;

        return (
            <div>
                <div className="top-nav">
                </div>
                <div className="filters">
                    <label>
                        Country:
                        <select value={selectedCountry} onChange={this.handleCountryChange}>
                            {countries.map(country => (
                                <option key={country.code} value={country.code}>{country.name}</option>
                            ))}
                        </select>
                    </label>
                    <label>
                        Date Range:
                        <select value={yearRange} onChange={this.handleYearRangeChange}>
                            <option value={1}>1 year</option>
                            <option value={5}>5 years</option>
                            <option value={10}>10 years</option>
                            <option value={15}>15 years</option>
                            <option value={20}>20 years</option>
                        </select>
                    </label>
                </div>
                <div className="chart-container">
                    <div className="chart"><Graph1 selectedCountry={selectedCountry} yearRange={yearRange} /></div>
                    <div className="chart"><Graph4 selectedCountry={selectedCountry} yearRange={yearRange} /></div>
                </div>
                <div className='chart-container'>
                    {/* <div className="chart"><Graph3 selectedCountry={selectedCountry} yearRange={yearRange} /></div> */}
                </div>
            </div>
        );
    }
}

export default GraphComparison;
