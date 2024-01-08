import { Component } from 'react'
import React from 'react'
import { Link } from 'react-router-dom'
import Logo from '../../assets/images/logo.png'
import './navbar.css'

class Navbar extends Component {
  state = { clicked: false }
  handleClick = () => {
    this.setState({ clicked: !this.state.clicked })
  }
  render() {
    return (
      <>
        <nav>
          <div className="mylogo">
            <Link to={'/'}>
              <img src={Logo} alt="" />
            </Link>
          </div>

          <div>
            <ul
              id="navbar"
              className={this.state.clicked ? '#navbar active' : '#navbae'}
            >
          </ul>
          </div>
        </nav>
      </>
    )
  }
}
export default Navbar
