import MyNavbar from 'components/commons/MyNavar'
import React from 'react'

const CommonLayout = ({children, isNavbar}) => {
  return (
    <div className="bg-light" style={{minHeight: "100vh"}}>
        {isNavbar? <MyNavbar/> :null } 
        {children}
    </div>
  )
}

export default CommonLayout