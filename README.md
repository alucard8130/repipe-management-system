RESUMEN FINAL DEL PROYECTO
Sistema Interno Bilingüe para Empresa de Repipe y Plomería (California)
1️⃣ Visión general

Se desarrollará un sistema web interno, 100 % bilingüe (Inglés / Español) para una empresa en California dedicada a instalación, reparación y mantenimiento de tuberías (repipe).

El sistema será:

Exclusivo para la empresa (no comercial)

Operativo + financiero

Orientado a proyectos

Diseñado para control de costos reales y rentabilidad

Con transparencia controlada hacia el cliente

2️⃣ Problema que resuelve

La empresa actualmente trabaja con múltiples herramientas aisladas (Excel, Monday, QuickBooks, Dropbox, calendarios), lo que provoca:

Falta de visibilidad integral

Poca claridad en costos reales

Dependencia del Owner

Dificultad para tomar decisiones estratégicas

👉 El sistema se convierte en el núcleo operativo, financiero y de dirección del negocio.

3️⃣ Usuarios del sistema
Usuarios internos

Owner – dirección, márgenes, BI, control total

Admin – operación general

Sales Rep – clientes, proyectos, estimaciones

Plumbing Tech / Drywall Tech – órdenes, checklists, horas

Accounting – compras, pagos, facturación

Usuarios externos

Clientes residenciales (Homeowners)

HOA / Property Managers

4️⃣ Módulos del sistema
🧱 1. Clientes, Propiedades y Proyectos

Registro de clientes y propiedades

Creación de proyectos

Vista Project 360 con toda la información del proyecto

📋 2. Alcance, Estimación y Contrato

Catálogo de servicios bilingüe

Construcción de estimaciones

PDFs bilingües

Control de versiones

Contratos y documentos firmados

🛠 3. Operación (Work Orders)

Órdenes de trabajo por especialidad

Checklists operativos

Agenda de técnicos

Registro de avances internos

📦 4. Compras e Inventario (centralizado)

Catálogo de materiales

Proveedores

Órdenes de compra (PO)

Recepción de materiales

Control de stock por movimientos (Kardex)

Alertas de stock mínimo

📐 5. Material estimado vs real

Estimación de materiales por proyecto

Registro de consumo real

Comparación automática y alertas por desviación

⏱ 6. Mano de obra y tiempo

Registro de horas trabajadas

Costo por hora editable por proyecto

Costos congelados para auditoría

💰 7. Facturación y pagos

Facturas por proyecto

Pagos parciales

Control de saldos

Preparado para futura integración con QuickBooks

📊 8. Costeo y BI del Owner

Cálculo automático de:

Costo real de materiales

Costo real de mano de obra

Costo total

Precio de venta

Utilidad y margen

Comparativos estimado vs real

Alertas inteligentes:

Margen bajo

Retrasos

Sobreconsumo

Stock bajo

👀 9. Portal del Cliente (bilingüe)

Acceso mixto:

Login (HOA / Property Managers)

Link seguro (Homeowners)

El cliente puede ver:

Estatus del proyecto

Avance por milestones

Fechas

Documentos autorizados

Fotos de avance

Facturas y saldo (si se permite)

❌ Nunca ve costos internos ni datos sensibles.

5️⃣ Avance del trabajo (milestones)

El progreso se comunica de forma clara:

Scheduled

Plumbing Work

Drywall Repair

City Inspection

Completed

Visible tanto internamente como en el portal del cliente.

6️⃣ Arquitectura técnica (final)
Componente	Decisión
Backend	Django + Django REST Framework
Frontend	React + TypeScript
Base de datos	PostgreSQL
Hosting	Render
Documentos V1	Guardados en la BD (BYTEA)
Documentos V2	S3 (opcional, sin refactor)
Inventario	Centralizado (Kardex)
Idiomas	Bilingüe EN / ES nativo
Deploy	Docker / Render CI-CD
7️⃣ Bilingüismo (regla global)

UI, portal cliente, PDFs, catálogos y estatus → EN / ES

Idioma por usuario y por cliente

Nada “hardcodeado” en un solo idioma

8️⃣ Nivel del sistema (valor real)

Este sistema permite al Owner:

Saber qué proyectos dejan mayor margen

Detectar desperdicio de material

Controlar eficiencia del equipo

Ajustar precios con datos reales

Escalar el negocio sin perder control
