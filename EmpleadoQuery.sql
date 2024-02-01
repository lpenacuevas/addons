--empleado--
SELECT  '__import__.hr.employee_' + CAST(e.idPersona AS VARCHAR(255)) as id,
CASE 
WHEN s.Sexo like 'F%' THEN 'Female'
WHEN s.Sexo like 'M%' THEN 'Male'
ELSE ''
END AS gender,  
CASE 
WHEN e.EstadoCivil like 'S%' THEN 'Single'
WHEN e.EstadoCivil like 'C%' THEN 'Married'
WHEN e.EstadoCivil like 'U%' THEN 'Legal Cohabitant'
WHEN e.EstadoCivil like 'V%' THEN 'Widower'
WHEN e.EstadoCivil like 'D%' THEN 'Divorced'
ELSE ''
END AS marital,
e.DocumentoIdentificacion as identification_id, 
e.Codigo as device_id, e.Nombre as [name], e.Apellidos as last_name, CONVERT(varchar, e.FechaNacimiento, 23) as birthday,
p.LugarNacimiento place_of_birth, p.CasoEmergencia as emergency_contact, p.CasoEmergenciaTelefono as emergency_phone, '__export__.employee_types_' + CAST(e.idTipoEmpleado AS VARCHAR(255)) as 'tipo_empleado/id',
e.Sueldo Salary, 
CASE 
WHEN e.idPersona = 1073  THEN NULL
ELSE CAST('' AS XML).value('xs:base64Binary(xs:hexBinary(sql:column("p.Foto")))', 'VARCHAR(MAX)')
END AS Imagen,
e.LaborandoEstado, e.LaborandoEstadoMes, '__export__.hr_job_' + CAST(e.idEmpleadoCargo AS VARCHAR(255)) as 'job_id/id',
CASE 
WHEN e.idTipoCondicion IS NULL  THEN '__export__.condition_types_1'
ELSE '__export__.condition_types_' + CAST(e.idTipoCondicion AS VARCHAR(255)) END AS 'tipo_condicion/id' , e.idPersona id_mrh,
CASE 
WHEN es.Estatus like 'I%' THEN 'false'
WHEN es.Estatus like 'A%' THEN 'true'
END AS Active,
'__export__.hr_department_' + CAST(e.idUnidad AS VARCHAR(255)) as 'department_id/id',
e.FechaIngreso fecha_ingreso, e.FechaEgreso fecha_egreso
from vistaEmpleado as e
inner join Sexo as s
on s.id = e.idSexo
inner join Persona p 
on p.idPersona = e.idPersona
inner join Estatus as es
on es.idEstatus = e.idEstatus
where e.idEstatus =1 

--job position--
SELECT '__export__.hr_job_' + CAST(e.idEmpleadoCargo AS VARCHAR(255)) as id, e.Cargo as [name],
'__export__.occupational_group_' + CAST(e.idEmpleadoPosicion AS VARCHAR(255)) as 'grupo_id/id', 
'__export__.cargo_viatico_' + CAST(e.idEmpleadoCargoViatico AS VARCHAR(255))  as 'group_positions/id',
e.idEmpleadoCargo as id_mrh
FROM EmpleadoCargo e


--cargo viatico--
SELECT '__export__.cargo_viatico_' + CAST(v.idEmpleadoCargoViatico AS VARCHAR(255)) as id, v.Grupo as [name],
v.Desayuno, v.Almuerzo, v. Cena, v.Alojamiento, v.idEmpleadoCargoViatico as id_mrh
FROM EmpleadoCargoViatico v
--Turnos--
SELECT 
	Tanda,
  ds.[horas de labor],
  t.HoraDesde [horas de labor/Work from],
  t.HoraHasta [horas de labor/Work to]
FROM 
  (
    SELECT 1 AS DiaSemana, 'Lunes' AS [horas de labor]
    UNION SELECT 2, 'Martes'
    UNION SELECT 3, 'Miércoles'
    UNION SELECT 4, 'Jueves'
    UNION SELECT 5, 'Viernes'
    UNION SELECT 6, 'Sábado'
    UNION SELECT 7, 'Domingo'
  ) ds
  CROSS JOIN Turno t

ORDER BY DiaSemana


--Grupo Ocupacionales--

select '__export__.occupational_group_' + CAST(ep.idEmpleadoPosicion AS VARCHAR(255)) as id,
ep.Posicion [name], 
CASE 
WHEN ep.Nivel=''  THEN 'NONE'
ELSE ep.Nivel
END AS nivel,
ep.Ponderacion ponderacion, ep.idEmpleadoPosicion id_mrh  from EmpleadoPosicion ep


--Localidades---
select '__export__.localidades_localidades_' + CAST(l.idLocalidad AS VARCHAR(255)) as id, 
l.Localidad [name], 
CASE 
WHEN l.Direccion IS NULL THEN ''
ElSE l.Direccion
END AS direccion, 
CASE 
WHEN l.Telefono IS NULL THEN ''
ElSE l.Telefono
END AS  telefono,  l.idLocalidad id_mrh from Localidad l

--pisos--
select '__export__.localidad_piso_' + CAST(p.idPiso AS VARCHAR(255)) as id, p.Piso [name], p.PisoNumero numero, p.idPiso id_mrh  from Piso p 

--tipos empleados-- 
select '__export__.employee_types_' + CAST(te.idTipoEmpleado AS VARCHAR(255)) as id, te.TipoEmpleado, te.idTipoEmpleado id_mrh from TipoEmpleado te

--tipo condicion empleado--
select '__export__.condition_types_' + CAST(tc.idTipoCondicion AS VARCHAR(255)) as id, tc.TipoCondicion, tc.idTipoCondicion id_mrh from TipoCondicion tc

--Unidades--
SELECT '__export__.hr_department_' + CAST(u.idUnidad  AS VARCHAR(255)) as id,
u.Unidad as [name],
CASE
WHEN u.Abreviatura IS NULL  THEN 'NONE'
ELSE u.Abreviatura END AS  abreviatura,
'__export__.localidades_localidades_' + CAST(l.idLocalidad AS VARCHAR(255)) as 'localidad_id/id',
CASE
WHEN u.idPiso = 0  THEN '__export__.localidad_piso_5'
ELSE '__export__.localidad_piso_' + CAST(u.idPiso AS VARCHAR(255)) 
END AS 'piso_id/id', 
CASE
WHEN idUnidadDependiente = 0  THEN NULL
ELSE '__export__.hr_department_' + CAST(idUnidadDependiente AS VARCHAR(255))
END AS 'parent_id/id', idUnidad as id_mrh,
CASE 
WHEN idPersona = 0  THEN NULL
ELSE'hr.employee_' + CAST(idPersona AS VARCHAR(255))
END AS 'manager_id/id'
FROM Unidad as u
inner join Localidad as l
on l.idLocalidad = u.idLocalidad

