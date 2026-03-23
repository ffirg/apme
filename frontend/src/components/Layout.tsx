import type { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { useTheme } from "../hooks/useTheme";

interface LayoutProps {
  children: ReactNode;
}

const NAV_ITEMS = [
  { path: "/new-scan", label: "New Scan", icon: "+" },
  { path: "/", label: "Dashboard", icon: "\u25A0" },
  { path: "/scans", label: "Scans", icon: "\u2630" },
  { path: "/violations", label: "Top Violations", icon: "\u26A0" },
  { path: "/fix-tracker", label: "Fix Tracker", icon: "\u2692" },
  { path: "/ai-metrics", label: "AI Metrics", icon: "\u2606" },
  { path: "/health", label: "Health", icon: "\u2665" },
];

export function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const { theme, toggle } = useTheme();

  const isActive = (path: string) => {
    if (path === "/") return location.pathname === "/";
    return location.pathname.startsWith(path);
  };

  return (
    <div className="apme-page-wrapper">
      <nav className="apme-sidebar">
        <div className="apme-sidebar-header">
          <div className="apme-sidebar-logo">A</div>
          <span className="apme-sidebar-title">APME</span>
        </div>
        <ul className="apme-nav">
          {NAV_ITEMS.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`apme-nav-item ${isActive(item.path) ? "active" : ""}`}
              >
                <span style={{ width: 20, textAlign: "center" }}>
                  {item.icon}
                </span>
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <div style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: "100vh" }}>
        <div className="apme-topbar">
          <div style={{ flex: 1 }} />
          <button
            className="apme-theme-icon-btn"
            onClick={toggle}
            title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            aria-label="Toggle theme"
          >
            {theme === "dark" ? "\u2600\uFE0F" : "\u263D"}
          </button>
        </div>
        <main className="apme-main">{children}</main>
      </div>
    </div>
  );
}
