import { useState, useEffect } from 'react';
import EcosystemShell from './pages/EcosystemShell';
import AboutPage from './pages/about';
import ContactPage from './pages/contact';
import CommunityPage from './pages/community';
import DocsPage from './pages/docs';
import PrivacyPage from './pages/privacy';
import TermsPage from './pages/terms';
import './index.css';

function Router() {
  const [path, setPath] = useState(window.location.pathname);

  useEffect(() => {
    const onPop = () => setPath(window.location.pathname);
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  const navigate = (href: string) => {
    window.history.pushState({}, '', href);
    setPath(href);
    window.scrollTo(0, 0);
  };

  // Expose navigate globally for links
  useEffect(() => {
    (window as any).__navigate = navigate;
    const handleClick = (e: MouseEvent) => {
      const target = (e.target as HTMLElement).closest('a[href]');
      if (target) {
        const href = target.getAttribute('href');
        if (href && href.startsWith('/') && !href.startsWith('//')) {
          e.preventDefault();
          navigate(href);
        }
      }
    };
    document.addEventListener('click', handleClick);
    return () => {
      document.removeEventListener('click', handleClick);
      delete (window as any).__navigate;
    };
  }, []);

  switch (path) {
    case '/about': return <AboutPage />;
    case '/contact': return <ContactPage />;
    case '/community': return <CommunityPage />;
    case '/docs': return <DocsPage />;
    case '/privacy': return <PrivacyPage />;
    case '/terms': return <TermsPage />;
    default: return <EcosystemShell />;
  }
}

export function App() {
  return <Router />;
}

export default App;
