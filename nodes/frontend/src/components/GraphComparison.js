// GraphComparison.js
import React, { Component } from 'react';
import Graph1 from './Graph1';
import Graph3 from './Graph3'; 
import Graph4 from './Graph4';
import axios from 'axios';
import './GraphComparison.css';

class GraphComparison extends Component {
    constructor(props) {
        super(props);
        this.state = {
            countries: [],
            selectedCountry: '',
            yearRange: 5,
            isLoggedIn: !!localStorage.getItem('token'),
            extreme_type: 'max', 
            years: 5
        };
    }

    componentDidMount() {
        if (this.state.isLoggedIn) {
            this.fetchCountries();
        } else {
            console.error('User is not logged in.');
        }
    }

    fetchCountries = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('http://127.0.0.1:8001/api/country', {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });
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
    
    handleExtremeTypeChange = (e) => {
        this.setState({ extreme_type: e.target.value });
    };

    handleYearChange = (e) => {
        this.setState({ years: parseInt(e.target.value, 10) });
    };

    handleLogout = () => {
        localStorage.removeItem('token');
        this.setState({ isLoggedIn: false });
    };

    render() {
        const { countries, selectedCountry, yearRange, isLoggedIn, extreme_type, years } = this.state;

        if (!isLoggedIn) {
            return (
                <div>
                    <p>Please log in to view the graphs.</p>
                </div>
            );
        }

        return (
            <div>
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
                <div className="filters">
                    <label>
                        Extreme Type:
                        <select value={extreme_type} onChange={this.handleExtremeTypeChange}>
                            <option value="max">Max</option>
                            <option value="min">Min</option>
                        </select>
                    </label>
                    <label>
                        Years:
                        <select value={years} onChange={this.handleYearChange}>
                            <option value={1}>1 year</option>
                            <option value={5}>5 years</option>
                            <option value={10}>10 years</option>
                            <option value={15}>15 years</option>
                            <option value={20}>20 years</option>
                        </select>
                    </label>
                </div>
                <div className="chart-container">
                    <div className="chart"><Graph3 extreme_type={extreme_type} years={years} /></div>
                </div>
            </div>
        );
    }
}

export default GraphComparison;
