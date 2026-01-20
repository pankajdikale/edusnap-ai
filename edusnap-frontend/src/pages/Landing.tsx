import { useNavigate } from 'react-router-dom';
import logo from '../assets/edusnap-logo.png'; // Add your large logo image to src/assets/

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      textAlign: 'center',
      padding: '20px'
    }}>
      <div style={{
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '50px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        maxWidth: '600px',
        width: '100%'
      }}>
        <img src={logo} alt="EduSnap Logo" style={{
          width: '300px',  // Increased from 120px
          height: 'auto',
          marginBottom: '10px',
          filter: 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3))'
        }} />
        <h1 style={{
          fontSize: '3rem',
          marginBottom: '20px',
          marginTop: '0px',
          fontWeight: '700',
          textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)'
        }}>
          EduSnap AI
        </h1>
        <p style={{
          fontSize: '1.2rem',
          marginBottom: '40px',
          fontWeight: '300',
          lineHeight: '1.6'
        }}>
          Revolutionizing attendance with cutting-edge AI-powered face recognition technology.
        </p>
        <button
          className="button"
          onClick={() => navigate('/login')}
          style={{
            fontSize: '1.1rem',
            padding: '15px 30px',
            borderRadius: '30px',
            fontWeight: '600',
            textTransform: 'uppercase',
            letterSpacing: '1px'
          }}
        >
          Get Started
        </button>
      </div>
    </div>
  );
};

export default Landing;