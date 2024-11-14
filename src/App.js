//app.js
import React, { useState, useEffect } from 'react';
import './App.css';
import { Pie, Bar } from 'react-chartjs-2'; // Importar Bar para el gráfico de barras
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

// Registrar los componentes de Chart.js necesarios
ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

function App() {
  const [resultados, setResultados] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mesSeleccionado, setMesSeleccionado] = useState(null);
  const colores = ['#FFA500', '#00FF00', '#FF0000', '#D2691E'];

  const meses = [
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
  ];

  const obtenerArchivoMes = (mes) => {
    return `filtrado_${mes}.csv`;
  };

  const cargarResultados = (mes) => {
    const archivoSeleccionado = obtenerArchivoMes(mes);
    setLoading(true);
    setMesSeleccionado(mes);

    fetch(`http://localhost:5000/resultados?archivo=${archivoSeleccionado}`)
      .then((response) => response.json())
      .then((data) => {
        setResultados(data);
        setLoading(false);
      })
      .catch((error) => {
        setError('Error al cargar los resultados');
        setLoading(false);
      });
  };

  const filtrarDatos = (resultados) => {
    const datosFiltrados = {};
    for (let clave in resultados) {
      if (resultados[clave] > 0) {
        datosFiltrados[clave] = resultados[clave];
      }
    }
    return datosFiltrados;
  };

  const obtenerDatosGrafico = () => {
    if (!resultados) return {};
    const resultadosFiltrados = filtrarDatos(resultados);
    return {
      labels: Object.keys(resultadosFiltrados),
      datasets: [
        {
          label: 'Resultados del Trading',
          data: Object.values(resultadosFiltrados),
          backgroundColor: colores,
          hoverOffset: 4,
        },
      ],
    };
  };

  // Para manejar el mes actual y ocultar noviembre/diciembre según corresponda
  const [mesActual, setMesActual] = useState(null);

  useEffect(() => {
    const fechaActual = new Date();
    setMesActual(fechaActual.getMonth()); // Guardamos el mes actual
    const mesAnterior = (fechaActual.getMonth() === 0) ? 11 : fechaActual.getMonth() - 1;
    cargarResultados(meses[mesAnterior]);
  }, []);

  return (
    <div className="App">
      <h2>Resultados del Trading</h2>

      {/* Ventana flotante de "Cargando..." */}
      {loading && (
        <div className="loading-modal">
          <div className="loading-content">
            <p>Cargando resultados...</p>
          </div>
        </div>
      )}

      <div>
        <h3>Selecciona un mes:</h3>
        <div>
          {meses.map((mes, index) => {
            // Lógica para ocultar noviembre hasta diciembre y diciembre hasta enero
            if ((index === 10 && mesActual !== 11) || (index === 11 && mesActual !== 0)) {
              return null; // No mostrar noviembre hasta diciembre ni diciembre hasta enero
            }
            return (
              <button key={mes} onClick={() => cargarResultados(mes)}>
                {mes}
              </button>
            );
          })}
        </div>
      </div>

      {error && <p className="error">{error}</p>}
      {resultados && (
        <div className="resultados-container">
          <div className="datos-container">
            <h3>Datos del Mes: {mesSeleccionado}</h3>
            <ul className="datos-list">
              {Object.keys(resultados).map((clave) => {
                if (resultados[clave] > 0) {
                  return (
                    <li key={clave} className={clave}>
                      {clave.charAt(0).toUpperCase() + clave.slice(1)}: <span>{resultados[clave]}</span>
                    </li>
                  );
                }
                return null;
              })}
            </ul>
          </div>

          <div className="grafico-container">
            <div className="grafico-torta">
              <h3>Gráfico de Tortas</h3>
              <Pie data={obtenerDatosGrafico()} />
            </div>

            <div className="grafico-barras">
              <h3>Gráfico de Barras</h3>
              <Bar data={obtenerDatosGrafico()} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;