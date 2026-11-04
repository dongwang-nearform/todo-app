import { NavLink, Outlet } from 'react-router-dom'

export function Shell() {
  return (
    <div className="app">
      <nav className="nav" aria-label="Surfaces">
        <NavLink to="/">Today</NavLink>
        <NavLink to="/not-done">Not done</NavLink>
        <NavLink to="/lists">Lists</NavLink>
        <NavLink to="/period">Period</NavLink>
      </nav>
      <Outlet />
    </div>
  )
}
