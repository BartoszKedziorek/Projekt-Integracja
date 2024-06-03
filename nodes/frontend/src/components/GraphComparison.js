import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Graph1 from './Graph1'; // Adjust the import path as necessary
import Graph3 from './Graph3';
import Graph4 from './Graph4';
import Logout from './Logout'; // Import Logout component
import './GraphComparison.css'; // Import the CSS file for styling

class GraphComparison extends Component {
    constructor(props) {
        super(props);
        this.state = {
            countries: ['USA', 'India', 'Germany', 'China'],
            selectedCountry: 'USA',
            yearRange: 5,
            isLoggedIn: !!localStorage.getItem('token') // Check if the user is logged in
        };
    }

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
        return (
            <div>
                <div className="top-nav">
                </div>
                <div className="filters">
                    <label>
                        Country:
                        <select value={this.state.selectedCountry} onChange={this.handleCountryChange}>
                            {this.state.countries.map(country => (
                                <option key={country} value={country}>{country}</option>
                            ))}
                        </select>
                    </label>
                    <label>
                        Date Range:
                        <select value={this.state.yearRange} onChange={this.handleYearRangeChange}>
                            <option value={1}>1 year</option>
                            <option value={5}>5 years</option>
                            <option value={10}>10 years</option>
                            <option value={15}>15 years</option>
                            <option value={20}>20 years</option>
                        </select>
                    </label>
                </div>
                <div className="chart-container">
                    <div className="chart"><Graph1 selectedCountry={this.state.selectedCountry} yearRange={this.state.yearRange} /></div>
                    <div className="chart"><Graph4 selectedCountry={this.state.selectedCountry} yearRange={this.state.yearRange} /></div>
                </div>
                <div className='chart-container'>
                    <div className="chart"><Graph3 selectedCountry={this.state.selectedCountry} yearRange={this.state.yearRange} /></div>
                </div>
            </div>
        );
    }
}

export default GraphComparison;
