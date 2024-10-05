# 📖TTPS-(Opción E)

### 📅 Cronograma

| Fecha Martes | Martes (Responsable, Modalidad) | Fecha Miércoles | Miércoles (Responsable, Modalidad) |
|--------------|---------------------------------|-----------------|-----------------------------------|
| 17/Sep       | Cecilia, Presencial             | 18/Sep          | Cecilia, Presencial               |
| 24/Sep       | Cecilia, Presencial             | 25/Sep          | Cecilia, Presencial               |
| 1/Oct        | Cecilia, Presencial             | 2/Oct           | Leandro, Virtual                  |
| 8/Oct        | Cecilia, Virtual                | 9/Oct           | Leandro, Virtual                  |
| 15/Oct       | Matias, Presencial              | 16/Oct          | Leandro, Virtual                  |
| 22/Oct       | Matias, Virtual                 | 23/Oct          | Leandro, Virtual                  |
| 29/Oct       | Matias, Presencial              | 30/Oct          | Leandro, Virtual                  |
| 5/Nov        | Matias, Virtual                 | 6/Nov           | Leandro, Virtual                  |
| 12/Nov       | Matias, Presencial              | 13/Nov          | Leandro, Virtual                  |
| 19/Nov       | Matias, Presencial              | 20/Nov          | Leandro, Virtual                  |
| 26/Nov       | Matias, Virtual                 | 27/Nov          | Leandro, Virtual                  |
| 3/Dic        | Matias, Presencial              | 4/Dic           | Leandro, Virtual                  |

---

Esta materia fue un desastre en cuanto a los links asi que voy a mandarlos aca en orden.

Miercoles 4 de septiembre
- https://www.youtube.com/watch?v=DLQeqMaHVYs
- https://en.wikipedia.org/wiki/From_the_Earth_to_the_Moon_(miniseries)
- https://www.scrumio.com/blog/cynefin-framework/

Jueves 5 de Septiembre
- https://docs.google.com/document/d/1E0lR0sUQfTdxJQHPwQfl0iMKtLxL6IeriBcBaO_WQFQ/edit

Lunes 9 de Septiembre
Tengo que instalar telegram (que pesados)
- https://docs.google.com/document/d/1oJW7QoK1SNUlUR4lMIzBRSPuiE1I_cgK3JHuFaVavUQ/edit
- https://docs.google.com/presentation/d/1PVn8KV_7YS3ovhIKth5cjYgVtesg2S5J5C_BHRJIaEo/edit?usp=sharing
- Telegram: https://t.me/+-3kq3qx-3UI5ODJh
- Mail para reclamar: lanto2004@gmail.com

Actividades LEL y Escenarios

---

### Mensaje Importante

Hola,

Esta semana arrancaron con Cecilia, Matias y todo el equipo conociendo la app que deberan desarrollar a traves de una tecnica explicada por Cecilia. Quiero contarles que en paralelo con lo que vienen realizando con Cecilia y equipo, necesito que vayan elaborando lista de simbolos LEL y Escenarios que valgan la pena describir para esta app.

Necesito que por favor:

(i) pidan acceso al siguiente google folder

https://drive.google.com/drive/folders/1e7THu5Kv_l5PWlxn87FVA8bYF3vgyom6?usp=drive_link

(ii) hay 5 documentos, cada grupo debe trabajar en su google doc, conforme la numeracion de los grupos que se encuentra en los siguientes slides

https://docs.google.com/presentation/d/1PVn8KV_7YS3ovhIKth5cjYgVtesg2S5J5C_BHRJIaEo/edit#slide=id.g2fe62df3ec2_0_2

(iii) el primer trabajo es armar la lista de simbolos y escenarios. Es decir, no tienen que describirlos, simplemente tienen que listar que simbolos y escenarios tienen sentido describirlos. Deberian tener esto terminado para el Miercoles proximo.

---

Todas las clases

https://drive.google.com/drive/folders/1v7J9agEz6HanDioZyDRbHFunjoThQE8P

---

### 📚 Tratando de transcribir el audio que tuvieron el dia que falte

Cual va a ser el objetivo principal de la aplicación?

El objetivo es hacer la gestión de las muestras necesarias para poder hacer diagnostico de enfermedades raras. En particular de 5 enfermedades raras. Si quieren se las enumero.

> En teoria escribio las 5 enfermedades raras en el pizarrón

---

Tienen pensado algun nombre/logo?

Todavia no lo hemos definido. Asi que si me lo pueden proponer esta bien, me sirve.

---

Quienes van a ser los usuarios que van a usar la aplicación?

Tenemos pensado varios tipos de usuarios que participan en el proceso completo.
- El primer usuario seria el medico que deriva al paciente. (El medico derivante)

Imaginen que el paciente con ciertos sintomas se acerca al medico que vamos a llamar "medico derivante". El medico derivante sospecha de esta enfermedad rara y nos pide este estudio a nosotros como laboratorio. El primer usuario es este.

Despues va a haber otro usuario Administrador de nuestro laboratorio, que es el que va a hacer la gestion propiamente dicha del sistema.

Despues va a estar el paciente, que tambien va a poder acceder al sistema para poder hacer siertas cosas.

Y tambien va a haber un usuario que se encarga de transportar las muestras. Desde los centros de extracción hacia un lugar centralizado, desde donde se van a recoger para mandarse al exterior. En principio esos son los roles que se me ocurren por ahora, puede que despues se me ocurra otro.

---

A partir de estos roles, tenes pensado como va a ser el proceso de registro?. Que campos vamos a tener encuenta

El inicio lo tengo claro, despues lo demas lo podemos ir viendo juntos.

El inicio seria el `medico derivante`, dando de alta al paciente y los datos que tiene que cargar el paciente son:
- Dni
- Mail
- Nombre
- Apellido
- Fecha de nacimiento
- Los antecedentes Familiares
- Resumen de la historia clinica

Una aclaración que no les hice y es muy importante, es que las enfermedades raras, en general son enfermedades geneticas.

Entonces el registra/alta del paciente la va a hacer el profecional, da de alta al paciente y da de alta el pedido de estudio para ese paciente, ese seria el primer registro.

Ahora como el medico esta de alto en el sistema, lo podemos ir charlando juntos. Lo que a mi se me ocurrio es que alla un administrador de laboratorio que se encarga de dar de alta a los medicos. O sea que de alguna manera, a ese `administrador general` podemos llamarle, que no se los mencione en los roles pero podria ser un rol nuevo, le llega por mail la información de un medico y el se encarga de darlo de alta.

Asi que el registro incial seria de esa manera, alguien le da de alta al medico y el medico le da de alta a su paciente y al pedido. Que si quieren para unificar terminos, a ese pedido lo vamos a llamar `estudio`

---

Con lo que nos acabas de decir, pretendes que en el sistema haya dos tipos de administradores?

Si, uno seria el administrador de laboratorio/o de muestrra y el otro es el admin general que se encarga de dar de alta a esos usuarios.

---

Este administrador general es el que asigna los roles?

Exacto, excepto en el caso del paciente que a este se lo asigna el medico.

No me quiero meter en la parte informatica, pero a ese administrador general, si me preguntan quien lo da de alta, pueden asumir que se da de alta directamente desde la base de datos. Es un usuario que esta en la base de datos

---

Que funcionalidades va a tener cada tipo de usuario?

El `Medico derivante` como les comente, va a poder dar de `alta a los pacientes` y va a poder pedir `Estudio` para los `Pacientes`.

El `Administrador de Laboratorio` se va a encargar de hacer toda la gestion de la `Muestra`. Se los digo de manera general, despues si ustedes lo necesitan mas adelanter entramos en mas detalle.

El que `Hace el transporte` se va a encargar, eso lo van a trabajar con los usuarios especialistas en ese tema. Pero se van a encargar de retirar las muestras de cada uno de los centros de extracción para llevarlos al centro de recolección.

Despues el `administrador del laboratorio` se encarga de gestionar el envio al exterior y algunas cosas mas 

El `Paciente` va a poder elegir el turno para poder hacerse la extracción y otra funcionalidad que tiene que tener el paciente es `ver el resultado` cuando este listo.

El medico derivante tambien va a poder ver el resultado de sus pacientes

---

De solo sus pacientes?

Si, de solo sus pacientes

---

Todo este proceso, en que me mencionaste a los transportistas, que lo que hacecn es recoger las muestras, interactuan con el sistema en si? El `usuario tranportista` tendria que tener algún tipo de interacción con el sistema

Si, yo me estoy imaginando, me voy a meter en el terreno de algo que no voy a hacer yo, que lo van a hacer Alex y .... Porque los usuarios de esa aplicación son Alex y Bryan, Pero lo que te puedo decir es que va a tener que interactuar. Porque tiene que marcar de alguna manera, las muestras que recogio, en el centro de extracción y cuando las entrega en el laboratorio central. Las tiene que marcar como que fueron entregadas y que ya estan en el laboratorio central.

De esa parte se encarga el transportista. Ahora que es lo mas comodo para ese transportista, ya no lo se porque no conozco como trabajan en esa parte.

---

Estas muestras entregadas, le aparecerian al `administrador de laboratorio` tambien, para poder visualizarlas?

Exacto, yo lo que espero es que el `administrador del labotorio` en cualquier momento pueda saber en que estado esta, cada una de las muestras, Si yo fuera administrador de laboratorio, quiero ver una lista con todas las muestras, o poder hacer una busqueda rapida de una muestra por alguna caracteristica. Y poder ver en que estado esta. Ademas de todos los datos de la muestra.

Estamos hablando de muestra y estamos hablando de estudio si quieren  unifiquen los terminos, porque es lo mismo

> MUESTRA Y ESTUDIO ES LO MISMO

A partir de una muestra hacemos un estudio.

---

Que se registra de cada muestra o estudio? que datos

Bien, vamos a registrar.....

Los datos del paciente que ya les comente cuales son. Se va registrar la lista de sintomas que tiene el paciente. Que una particularidad es que, no quiero que la tenga que escribir, el medico, sino que la pueda seleccionar. Yo se que de alguna manera hay alguna forma de poner una lista de todos los sintomas, en algun lado esta, asi que si lo pueden investigar fijense. De donde lo pueden bajar para tener una lista. Y tiene que ser comodo poder escribirlo.

Imaginese que el medico esta con el paciente y el medico le pregunta que sintomas tenes, el paciente se lo empieza a expresar con sus palabras y el medico lo que hace es convertirlo en lenguaje medico. Y tiene que ir registrando cada uno de los sintomas. Eso por un lado

Por el otro va a indicar cual es la patologia. El estudio para que patologia lo quiere realizar. Cual es la patologia que sospecho cual de `ESTAS 5 QUE YA NOS DIO CON ANTERIORIDAD`

Y hay una cosa muy importante es que lo quiero ayudar al medico para que no pida un estudio pra algo que seguro no tiene que ver con el paciente.

Porque estos medicos que piden los estudios, no son `Medicos Genetistas`, son medicos mas generales, entonces no conocen en detalle las enfermedades geneticas, las pueden llegar a sopechar, pero desde el sistema yo le quiero dar una mano.

Entonces, van a disponer, nosotros ya compramos una API a la cual le van a poder pegar para poder saber, dada una patologia, cuales son  lo que llamamos nosostros `SINTOMAS CARDINALES` (Son como los sintomas principales que tienen estas enfermedades raras o cualquier enfermedad)

Uno de los endPoints que tiene esa API es, le paso esa patologia y me dice una lista de `Sintomas Cardinales (Principales)`

Entonces el sistema tiene que poder validar, cuando seleccionan la patologia. Que al menos uno de los `sintomas cardinales (Principales)` de esa patologia este presente/marcado dentro de los sintomas que eligio el medico. Sino no me deja pasar.

Eso si se trata de una sospecha puntual, es decir que es el primer paciente de toda la familia. Un paciente que no tiene historia familiar de ninguna de estas patologias pero es compatible con los sintomas. A eso le llamamos `Sospecha puntual`

Entonces el medico cuando da de alta al estudio tiene que marcar, que es una `sospecha puntual` 

Entonces decimes sospecha puntual para alguna de estas (asmd, Gaucher, mps 1(griego), fabry y pompe). Sim existe esa opción el sistema tiene que hacer esa validación.

Ahora puede ser que la consulta medica sea por alguna sospecha familiar, es decir que ya un primo, lo diagnosticaron con `fabry` y viene el paciente y no tiene ningun sintoma pero esta preocupado y el medico del primo le recomendo que venga a consultarse tambien

---

Estaria bueno que al momento en el que el medico registre un paciente, pedirle, justamente el historial clinico, ya estaria contemplado ahi. 

Esta bueno lo que decis, me gusta lo que pasa es que si en el resumen de la historia clinica. Esta escrito en lenguaje natural, es medio dificil poder captar de adentro que esto es una sospecha familiar entendes?????

Entonces yo lo que me imaginaba era algo como mas simple como una selección que pueda hacer el medico donde elije, si es una `sospecha puntual` o si es una `sospecha familiar`

Porque en la entrevista con el paciente, el paciente le va a decir el porque lo viene a ver.

El paciente dice: Vengo porque a mi primo le diagnosticaron `Fabry`

Entonces ya ahi, automaticamente, aunque no le vea ningun sintoma, el medico marca es una `sospecha familiar` quiero analizar si este paciente tiene `Fabryc`

---

Entonces respondiendo a tu pregunta, la pregunta original era 

Que tengo que cargar de un estudio????:

Ademas de dar de alta a los datos del paciente, tengo que cargar cuales son los sintomas, cual es la patologia y si es una `sospecha puntual` o si es una `sospecha familiar`, porque si es una sospecha familiar, la validación no es necesaria. Puede ser que tenga los sintomas o puede ser que no (eso no es importante si es por `sospecha familiar`). Esto lo hacemos asi para prevenir, y una de las caracteristicas que tienen estas enfermedades raras es que son `subdiagnosticadas`

Las caracteristicas de las `enfermedades raras` son

- Que son poco prevalentes (Poco frecuentes)
- Y que los sintomas son muy parecidos a otras patologias.

Entonces los medicos no la tienen como primera opción, piensan en muchas otras patologias antes y esta se olvida. 

Y son enfermedades que diagnosticadas temprano pueden tener una mejor evolución. Por eso es tan importante que podamos hacer una detección temprana, de estas 5 enfermedades raras y ademas porque tenemos tratamiento para estas enfermedades. 

---

Todo estos seguimientos que nos decis, las estaria siguiente solamente el medico de ese paciente??

Podria ser que no, (la puta madre) puede ser que hoy se testea para una patologia, da negativo y dentro de dos años quiere volver, su medico original, ya no lo atiende y quiere consultar otro medico y ese otro medico lo tiene que poder encontrar en el sistema al paciente, aunque lo haya dado de alta el medico original y poder cargar un estudio nuevo.

---

Entonces nos podrias contar como es el seguimiento de cada muestra/estudio en la aplicación?? que es que vos esperas??

Vos nombraste que el administrador del laboratorio tiene que poder serguir el estado de las muestras a lo largo de la aplicación, como es este seguimiento? (pregunta como el tuje xd)

El administrador del laboratorio como se desepña en el seguimiento de la muestra??

Por ejemplo que pase por distintos estados??

SI va a pasar por distintos estados

---

Cuales son los estados??

Lo primero que tiene que ocurrir.... voy a continuar con la primera parte y ustedes despues me preguntan mas

---

Una vez que el medico dio de alta el pedido/estudio, le tiene que aparecer en la lista de estudios al administrador del laboratorio y lo primero que tiene que hacer el administrador del laboratorio es, poder armar un presupuesto, porque alguien lo tiene que pagar al estudio.

Asi que, no se que es lo que necesitan saber de ese estado.

El segundo estado seria esto, `presupuesto armado`

Que necesitan saber de eso??

---

Del presupuesto, los campos mas alla del monto, un detalle del presupuesto.

Yo lo que necesito es..... Eso lo podemos discutir si lo da de alta el `Administrativo` o si ya lo dio de alta el `medico` 

Ademas de los campos que ya les dije, tenemos que poner:

- Cual es el tipo de estudio que hay que hacer, siempre va a ser el mismo estudio que se llama `Exoma`. Esta bien que lo dejemos como campo porque estamos pensando en expandirnos a otros tipos de estudio, pero por ahora el estudio que se hace es el `Exoma` para hacer el diagnostico.
- Despues la lista de genes que tengo que analizar, porque el ADN, es como una palabra muy larga, de 30 mil millones de letras, donde cada posicion de esa palabra puede ser una A, una C, una T o una G. Y hay ciertas regiones en esa gran palabra, que son distinguidas, que se llaman ``genes``, porque codifican las instrucciones para generar una `Proteina`. Que la proteina son las que llevan la función en nuestro organismo. Existe tambien lo que se llama como `genoma de referencia humano` que nos dice para cada posición, cual es la letra mas representativa (la letra normal). Entonces yo comparando los genes de un paciente (las letras de gen de un paciente) con los genes normales. Puedo detectar si hay algún gen mutado. Si ese gen esta mutado. Puede ser la causa de la enfermedad. Para cada una de estas enfermedades yo ya se cual es el o los genes que se mutan. Entonces lo que yo tengo que especificar es cual es: Cuales son los genes que yo quiero evaluar del paciente y para eso en la API que les comente, tienen  un EndPoint al cual le mandan la patologia y le devuelve la lista de genes.
- Otra cosa importante que tenemos que registrar es: siempre que se hace un estudio genetico por mas que vayamos a buscar esos genes especificos de las patologias. Se pueden evaluar lo que se llaman los `hallazgos secundarios`, es decir, genes que se analizan siempre porque son accionables. Yo puedo hacer algo si descubro que hay una mutación en esos genes aunque no haya ningun sintoma en el paciente. Entonces una marquita mas que yo tengo que hacer en el estudio es si el paciente acepta que evaluemos los `hallazgos secundarios`, es decir ademas de los genes para evaluar esta patologia si evaluo los `hallazgos secundarios`
- Y por ultimo lo que tiene que tener el presupuesto, quiza esos dos campos que les dije recien, podrian ser parte del estudio, cuando se da de alta el estudio, no necesariamente en esta estapa del armado del presupuesto (porque son datos del estudio) fijense que les parece 

---

La primera parte, la cargaria el medico y la parte del presupuesto solo el administrador?

Claro, pero fijate que, el tipo de estudio el medico lo sabe, con lo cual lo podriamos poner del lado del medico y la lista de genes se calcula automaticamente a partir de las patologias con lo cual tambien lo podemos llenar.

Yo originamente lo pense como que lo iba a hacer el administrador, pero lo puede hacer en el momento en el que se crea el estudio.

Lo que si no puede hacer o confirmar el medico es el presupuesto propiamente dicho. Entonces el administrador si que tiene que tener una opción en el sistema para poder generar ese presupuesto a partir del estudio que cargo el medico.

Y para eso tenemos una regla, para generar ese presupuesto, que despues la tiene que aceptar el administrador, pero la regla es. El sistema le va a sugerir un presupuesto y despues el administrador la puede modificar y le puede poner un presupuesto distinto.

Y la regla es la siguiente:

El costo del `Exoma` es 500$ de base e incluye el analisis de 5 genes.

Cualquiere gen adicional se cobra 30$, eso es lo que tieen que calcular automaticamente el sistema y se lo tiene que tirar en la pantalla de alguna manera al administrador y el administrador termina aceptando o modificando. Y eso me tiene que generar un PDF porque si lo tengo que entregar al paciente para que lo lleve a la obra social para que se lo aprueben o para que lo pague de manera particular de todas maneras, como tengo un area de pagos no me quiero meter en el lio de manejar los pagos en el sistema. En algun momento me va a llegar un mail o algo donde me garanticen que el pago ya se hizo y yo lo tengo que `registrar en el sistema`, pero no me importa a mi, si lo pago la obra social o lo pago particular o lo pago otro laboratorio o quien lo pago.

---

Ese seria por decirlo asi, el segundo estado??

Claro, o el segundo paso, que es el primero del administrador. Que lo dio de alta el medico, en el momento en el que se da de alta se calcula todo lo que digimos recien y ya le aparece en la lista al administrador del laboratorio y lo primero que tienen que hacer es generar el presupuesto. 

Tengan en cuenta que el administrador del laboratorio tiene que tener alguna manera agil. Tiene que saber que le entro un estudio nuevo para trabajar o tiene que tener alguna bandeja de entrada o una bandeja de trabajo que le resulte sensillo para saber que es lo que tiene que hacer, que es lo que esta esperando por el. Eso me gustaria que exista. 

Bueno y despues una vez como les comente, le llega el mail avisandole que ya el pago se realizo, lo unico que hace es `registrar el pago`. 

---

Quien registra el pago??

El administrador del laboratorio. El circuito por el cual el administrador se entero que realizo el pago, no nos interesa (VAMOOOOOOOOOOOOOOOO), porque eso lo maneja el area de pagos y yo no me quiero meter con eso.

Si me quieren ofrecer algo tipo online o algo asi, bueno lo charlamos pero en principio no lo necesito

---

Del pago se registra algo importante??

No, que se pago y listo 

---

Cual seria el siguiente estado??

Bueno, ahi me gustaria que se involucre el paciente. Porque lo proximo que sigue, es poder elegir el turno. Y elegir el turno implica, elegir alguno de los 100 centros de extracción que tenemos, en `La Plata`, `Capital Federal ` y `El Gran Buenos Aires`, todos nuestros centros de extracción estan distribuidos por ese lugar y tiene que elegir `Hora` y `Dia`. Los turnos duras `15 minutos`, cuando se ocupa un slot, lo toma un paciente y se ocupan esos `15 minutos`.

No se como lo podemos pensar esto, pero a mi me gustaria que eso, lo haga directamente el paciente. En alguna aplicación web, no que tenga que llamar por telefono al paciente o que mi gente del laboratorio tenga que llamar al paciente para preguntarle que dia le queda bien. Entonces que el paciente entre de alguna manera al sistema y pueda elegir el centro de extracción, el dia y la hora, que este libre obviamente. Porfavor no le den el mismo turno a dos pacientes, porque se empieza a acumular gente y eso siempre me trae problemas. Asique eso es MUY MUY IMPORTANTE

La experiencia de usuario para el paciente es muy importante porque sino se nos van con la competencia :(

Lo que si necesito que suba el paciente es:

El consentimiento informado, de que quiere hacerse este estudio, porque parte del estudio lo mandamos a hacer afuera, la lectura del adn, la hacemos en Corea, necesito que el paciente me autorice a mandar, su muestra de sangre al exterior y que pase por la duana. 

Si quieren yo les puedo dar un consentimiento firmado para que lo cuelguen en algun lado, de manera que el paciente lo pueda bajar, firmar, y que cuando confirma el turno, lo pueda subir.

No se si necesitan saber algo mas del paciente.

---

A la hora de que el paciente va y hace la extracción, queda algo registrado del punto a donde se manda esa  extracción?

Bueno, eeeeeeeeeeeeeeeeeeeeeeeeeeeeee. NO 

No necesitamos, lo unico que de alguna forma, el estudio ese tiene que quedar marcado como que ya se tomo la muestra de ese paciente.

Eso quien les parece que lo podria cargar?? (Lo ignoramos completamente y nadie respondio xd)

---

La idea de la aplicación es que todos los laboratorios tengan acceso al sistema? o solamente el laboratorio que se encarga de centralizar las muestras?

Yo pensaba que sea solamente el laboratorio central, pero el tema es que como el laboratorio central se entera de que ya le tomaron la muestra a este paciente.

No me importa registrar ningun dato de la toma de muestra, simplemente que quede marcada como tal, la muestra para que el transportista la pueda tener en su hoja de ruta. Piensenlo a ESO (pta madre we) a ver que se les ocurre, alguien lo tiene que hacer.


---

Una vez que la muestra fue marcada como `tomada` le va a parecer en la hoja de ruta al `transportista`.

Bueno, esta parte ya la conte, el transportista tiene que marcar esos dos estados, que uno es `Recolectada` y el otro es `Liberada` o dejada en el laboratorio central.

Lo de la hoja de ruta a mi me gustaria que sea inteligente, pero eso se lo dejo a lo chicos, cuando lo hagan con `Bryan` y `Alex` que ellos ya tiene experiencia, con otras aplicaciones del estilo. 

No me importa a mi, lo unico que quiero que sea es eficiente.

---

El laboratorio que mensionabas en Corea, va a tener algún tipo de comunicación con la aplicación? o solamente el administrador se encarga de los envios y se desentiende?? 

Es una buena pregunta, en realidad todavia ni siguiera llegamos a corea (menos mal)

A tu pregunta, no vamos a tener contacto desde el sistema con el laboratorio de Corea. Nosotros vamos a recibir un mail. 

Nos salteamos varios pasos pero te respondo ya que me preguntaste. `Vamos a recibir un mail con el resultado`

Y el administrador del laboratorio se va a encargar de cargar el resultado en el sistema. 

La recepción del resultado es por otra via, no por el sistema. Porque lo intentamos y es mucho quilombo.

---

Una vez que se esta en el laboratorio central, en otros estados pasaria la muestra?

Aca hay una particularidad de que, los envios, los tenemos que hacer de a `100 muestras` No se mandan paquetes de a `1 muestra`, sino que tengo que `mandar de a 100 muestras`. Los Envios hacia el exterior exacta,emte.

Una vez que estan en el `laboratorio central`, no puedo mandar 3 muestras solas, tengo que mandar minimo 100, maximo 100 digamos. 

Si en el laboratorio central tengo 45, tengo que esperar otras 55 para poder mandar el paquete y si tengo que esperar hasta mañana lo hago. Saben pora que??? Porque si mando menos de 100 me cobran el shiping, el envio y es carisimo. 

Entonces no esta calculado en los costos y entonces tenemos que esperar a tener 100 muestras.

Pueden ser mas de 100 si quieren, pero minimo son 100, SI O SI.

En la estrategias que usamos, es no mandar mas de 100, porque sino en el proximo Lote, tarda mas de lo que se deberia. Y si mandamos de a tandas de 100, todo es mas rapido.

Por ejemplo, si yo tengo 150 y mando los 150 juntos, despues voy a tener que esperar a tener otros 150 para poder armar otro grupo/paquete. 

A ese grupo de Muestras, de pedidos de estudio. Le llamamos `Sample set` (Conjunto de Muestras en ingles xd)

Y eso, me gustaria que sea automatico. No quiero a alguien detras, haber cuanto falta, o a partir de estos 100 armo un `Sample Set`, sino que el sistema de manera automatica, cuando llega al nro 100 arma un `Sample Set`. No se si se puede hacer eso, pero me gustaria.

---

O sea que a partir de que el transportista la marca como entregada que el sistema registre un contador de muestras y como te gustaria que se notifique eso??

⚠️⚠️ A Mi me gustaria que el `adminstrador del Laboratorio` tenga una vista de `Sample Sets`, de la misma manera que tiene una lista de los `Samples`,  que tenga una vista de los `Sample Sets`. Y que desde el `Sample Sets` yo pueda ver. El `Sample Set` va a tener tambien un estado particular y que yo pueda navegar en el `Sample Sets` los `Samples` que contiene. Es como que se arma y se desarma. (Podriamos armar una pagina por cada uno y que contenga una lista de estos)

Despues se van a volver a desarmar porque el resultado pertenece a cada estudio particular pero los agrupo para enviarlos y despues se vuelve a desarmar.

---

El transportista tiene interacción con el sistema web???

No necesita, si me van a dar una APP, no necesitamos

+ Para ver si va a tener perfil en la web porque eso quedo medio en la pregunta. 

Si asumimos que vamos a tener una APP, no. Si no tuviera la APP, lo tendriamos que hacer desde el sistema pero va a quedar bastante incomodo.

Importante que lo que termina haciendo desde la APP, tiene que impactar en el mismo backend que la aplicación WEB, no tienen que ser base de datos distintas ni nada de eso. Es una interfaz distinta NADA MAS.

---

#### Preguntas

Hablamos mucho de administradores, y mezclamos el concepto de administrador de laboratorio con el de administrador general. 

El administrador general que da de alta a los administradores de laboratorio y a los medicos, solo tendria que tener esa funcionalidad??

Si

Tendria la posibilidad de poder eliminarlos??

Si

Persona: Yo haria una baja logica, si queres que no se puedan dar de alta. Basicamente no quiero perder el historial, a eso voy, no hay que borrar los datos del paciente que halla cargado ese medico.

Lo podria marcar como Inactivo y LISTO.

Y si en un futuro quiere volver, lo activamos y listo.

---

Siguiendo con eso, te parece bien que el acceso sea con un nro de documento y que la primera vez que accede al ser con un nro de documento, que la cambie en el momento. 

Quien? 

El administrador de laboratorio, medico y paciente

Si, me parece buena idea.

---

Solo el administrador general esta precargado en la base de datos

---

Siguiedo tambien con el tema del acceso, yo podria tener un paciente que es menor de edad, puede accederlo de la misma manera o tiene que tener alguna restricción??

En ese caso lo suele hacer un tutor. Se registra el mail del tutor, el nro del tutor y nosotros le notificamos para que pueda acceder a la pagina y el que firma el concentimiento informado, es el tutor.

NO PUEDE FIRMAR UN MENOR AL CONSENTIMIENTO INFORMADO.

---

Ya que tenemos el administrador general y el del laboratorio, estos dos pueden dar de baja a los pacientes??

El administrador general es el que puede dar de alta, adminstrador de laboratorio y medicos. Y el administrador del laboratorio es el que hace todo este circuito del que venimos charlando.

---

Siguiendo con el paciente, el paciente recibio este presupuesto final, en caso de no querer porque le parece muy costoso y se va para otro lado. Se deberia informarse para nosotros finalizar el proceso??

Nunca me informan..

---

Te parece bien ponerle un tiempo estimado al presupuesto??

Me parece una buena idea, le podemos agregar una fecha de vigencia, que esa fecha de vigencia se calcula de manera automatica. En general la hacemos de 1 mes a es fecha de vigencia Y les tiro la idea y si la podemos hacer buenisimo. Si pueden pasar a un estado vencido al estudio cuando haya pasado el mes y no haya cambiado de estado el estudio, genial. 

⚠️⚠️ El medico tendria que pedir otra vez el turno (wtf, para mi deberia ser el paciente) Tendria que ir otra vez al medico..

---

Todos los registros tienen notificación por mail??

La verdad es que me da lo mismo siempre y cuando sea seguro. Si encuentran otra manera me da igual.

---

Si es menor de edad, que rol tendria el padre en la pagina al momento de registrarlo??

El medico tratante, el que recibio al paciente en la consulta, va a estar el nene de 2 años y va a estar el papá. Entonces cuando registra al paciente, el campo que dice mail, tiene que decir mail de contacto. Si son mayores de 18 tendra que decir `mail del paciente` y si son menores tiene que decir `mail del referente`. 

Era uno de los campos que les dije del paciente.

---

Del laboratorio a la central. El transportista todos los dias, tiene una hoja de ruta y lleva todas las muestras que se hicieron en el dia anterior.

---

Que sea el administrador del laboratorio el que marque se mando la muestra??

Lo incomodo de ahi es que voy a tener que resolver por mail es que el centro de extracción le avise al laboratorio. Pero esta bien, sino tendriamos que crear otro ROL, que sea de centro de extracción que se encargaria, pero no la compliquemos, porque estoy muy apurado con el sistema. Asi que acepto tu opción.

---

Asi que el centro de extracción se va a comunicar una vez que se tenga el registro de la muestra. Y el administrador del laboratorio la va a marcar como que esta lista para enviar porque ya se tomo la muestra. 

---

Llendo por el lado de las muestras, habiamos dicho que cuando tenemos una sospecha puntual, que no tiene relación, si yo en la API encuentro que no esta seleccionada con ninguna de las 5, deberia avisar??

Directamente no se puede crear el estudio

`La patologia que usted esta sospechando no es compatible con los sintomas marcados`

---

Los sintomas se pueden repetir para diferentes enfermedades??

Si

---

Tenes alguna preferencia con la paleta de colores??

Si, les puedo mandar el logo si quieren de la empresa pero, los colores son violetas. En la gamma de los violetas.

---

No me quedo claro que funcionalidades va a tener el transportista

Yo no se muy bien como trabajan ellos, lo que te puedo decir es que su responsabilidad es pasar a buscar las muestras por los centros de extracción todos los dias y llevarlas al laboratorio central. Para que en el laboratorio central se acumulen de a 100 y se puedan mandar al exterior. 

De que manera les conviene a ellos trabajar, no lo se, Bryan y Alex hace como 15 años que trabajan como transportistas asi que ellos se los van a poder comentar.

Ellos son los encargados de marcar la muestra como `ya la deje` en el laboratorio central para empezar, para empezar esa acumulación de a 100 muestras para mandarlas al exterior. 

---

Es importante mantener el seguimiento, porque la sede de extracción, avisa a la sede central. 

En el momento en el que el transportista, pasa a buscar esa muestra hace falta que se siga como por elemplo, "la muestra esta en proceso de envio" 

NO, NO LO NECESITO

---

El unico caso que puede pasar es que un estudio tenga solo una muestra, con un unico resultado.

SISISISISI.

---

No puede haber un caso en el que el medico diga, bueno, lo validamos con dos muestras.

NONO Eso no

Lo que si puede pasar, es que el ADN que se pudo extraer de la muestra de sangre, sea insuficiente. Porque el transportista se quedo tomando una gaseosa en el medio del sol y la sangre se desnaturalizo y cuando llega a corea, intentan sacar ADN y no hay.

En ese caso abria que tomarlo otra muestra al paciente. ⚠️⚠️stop, volver a cobrarle o como es eso?? Alta demanda le hago⚠️⚠️

---

Como te das cuenta??

En el resultado va a estar, pero vamos a dejarlo afuera eso tambien (GRACIAS DIOS)

En el caso de que eso paso, le decimos al paciente que vuelva a iniciar todo el circuito.

---

Corea nos informa por mail el resultado y el administrador del laboratorio se va ancargar de registrar el resultado, en nuestro sistema.

---

El resultado puede ser positivo, negativo o inconcluso?? 

No necesariamente, pueden ser 

- Baja calidad (no tengo resultado) y el laboratorio no me informa si se diagnostico o no la enfermedad, lo que me informa son las variantes geneticas que encontro, una variante genetica es como les comente. Cuando una letra en uno de los genes que analice, no coincide en esa misma posición con la letra de referencia al genoma de referencia. Imaginemos que el 90% de los humanos tenemos una letra `T` en esta posición y para este paciente en esa posición hay una `A`, a eso se le llama `Variante Genetica` es una variante respecto al genoma de referencia. Esa parte ya la tengo toda automatizada con lo cual. Porque el administrador del laboratorio va a recibir un mail por afuera, no me importa como, con las variantes geneticas. Y las variantes geneticas tienen un codigo que las identifica. Entonces lo que yo voy a informar si se realizo el estudio, es cuales son las variantes que se encontraron para ese paciente en particular, con su codigo.
Escribir esass variantes son un lio porque son codigos muy raros. Entonces no quiero que la tenga que escribir el administrador del laboratorio. Para eso se van a servir de la API nuevamente para poder obtener todas las variantes posibles. 

Algo que no me quedo claro, es que una muestra se envia al exterior, el del exterior manda el resultado y ese resultado es el que analizan los informaticos??

SI

Una vez que se envia al exterior, el administrador del laboratorio carga lo que serian las variantes geneticas.

El paciente no entiende nada de lo que son las variantes geneticas, entonces tenemos que decidir de alguna manera si el paciente tiene o no la enfermedad.

Para eso vamos a tener otro `EndPoint` que le dan la patologia y devuelve cuales son las variantes que se han identificado para esa patologia. Y ahi van a tener que machear, van a tener que buscar si hay alguna de las variantes que tenia el paciente que coincida con las variantes de la patologia.

- (la otra opcion ni la nombre)

--- 

El paciente en su perfil, ve sus patologias??

El paciente tiene que poder entrar y ver para cada estudio, un pdf con su resultado. El resultado lo tienen que poder bajar en pdf y tiene que decir BIEN GRANDE, POSITIVO, NEGATIVO Y abajo puede haber un informe que diga `se identifico la variante tal`.

Importante. Si el paciente habia aceptado los hallazgos secundarios, tambien se tienen que analizar esos genes e informarlos en el resultado final. 

Los hallazgos secundarios vienen del ADN en genes que ya estan predefinidos. 

Hay una serie de genes que si estan mutados, son accionables aunque no tengas ningun sintoma, entonces cada vez que se hace un estudio genetico, vos le preguntas al paciente.

Ademas de analizar lo que el medico le pide, quiere analizar estos otros genes para hallar estos hallazgos secundarios?

Si me dice que si, tambien los voy a tener que analizar.

---

Vamos a tener un `EndPoint` con la lista de variantes de todos los genes para hacer los hallazgos secundarios. 

Hacemos dos consultas

- Una consulta para una patologia determinada
- Una consulta para las variantes de los hallazgos secundarios.

Estaria bueno que el medico pueda acceder al resultado de sus pacientes solamente.

---

El ministerio de salud me exige tener que pedir una autorización, para enviar muestras de sangre, para poder sacar del pais muestras de sangre. De eso no me preguntaron nada pero se los comento porque me resulta IMPORTANTE.

Antes de poder mandar la muestra al exterior, tengo que conseguir esa autorización y para conseguir esa autorización. Ellos tienen una API en la que me hacen mandar un CSV con los datos de las 100 muestras (1 por `Sample set`) y me devuelve un PDF con la autorización.

Que dice, el ministerio de Salud autoriza a sacar las muestras de estos pacientes y una cosa muy importante es que, desde el momento en el que el medico, da de alta al estudio, los datos del paciente tienen que quedar Anonimisados para el administrador del laboratorio, el administrador del laboratorio no puede saber que Jose Perez se hizo el estudio. 

Me tienen que manejar algun codigo.

El codigo que me tienen que manejar es:

- un codigo auto incremental por ejemplo 1250_(las 3 primeras letras del apellido)_(las 3 primeras letras del nombre) y eso por confidencia, NO LO PUEDEN DEJAR PASAR, Si un administrador de laboratorio se enoja con nuestra empresa y publica todos los pacientes en el cual se sopecho `Fabry`, tenemos qeu cerrar el laboratorio 

PONGAN MUCHO FOCO EN ESO.

El unico que sabe el nombre del paciente es el medio.

En el centro de extracción les alcanza con saber el Codigo y en Corea tambien. 

Y los datos del paciente pueden ser vistos por el medico?? SISISI ESO ES FUNDAMENTAL

---

Puede pasar que cuando uno vaya a un medico, no le guste y despues vaya a otro en ese caso, como hacemos con los medicos que ya tienen acceso a ese paciente???

Eso es una buena pregunta, cuando este el resultado. Eso tendrian que ver como me lo resuelven.

Cuando se hace el cambio??

Yo voy al medico1 por ejemplo, el medico1 ya me cargo. No me gusto ese medico, me voy con el medico2 y el medico2 me carga y automaticamente quedaz desasociado del medico1, todo el tiempo el medico2 va a tener que continuar con el proceso de la muestra supongo. (DIOS QUE QUILOMBO OJALA NO LO HAGAMOS)

Esto no se podria hacer si la muestra esta en proceso, tendria que esperar a que la muestra termine por completo. Eso si TAL CUAL ()

---