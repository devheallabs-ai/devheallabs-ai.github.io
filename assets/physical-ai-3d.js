const reduced = matchMedia('(prefers-reduced-motion: reduce)');
async function mount(host) {
  try {
    const T = await import('./vendor/three.module.min.js');
    const canvas = host.querySelector('canvas'), viewport = host.querySelector('.stage-viewport');
    const renderer = new T.WebGLRenderer({canvas, antialias:true, alpha:true});
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = T.PCFSoftShadowMap;
    renderer.toneMapping = T.ACESFilmicToneMapping;
    const scene = new T.Scene();
    scene.fog = new T.Fog(0x101c30, 20, 48);
    const camera = new T.PerspectiveCamera(38, 1, .1, 80);
    scene.add(new T.HemisphereLight(0xb7d9ff, 0x273049, 3));
    const key = new T.DirectionalLight(0xffe7c3, 4);
    key.position.set(5,12,7); key.castShadow=true; key.shadow.mapSize.set(1024,1024);
    Object.assign(key.shadow.camera,{left:-14,right:14,top:14,bottom:-14});scene.add(key);
    const rim = new T.DirectionalLight(0x4e9eff,3);rim.position.set(-8,5,-5);scene.add(rim);
    const mat=(color,metalness=.3,roughness=.5)=>new T.MeshStandardMaterial({color,metalness,roughness});
    const white=mat(0xd8e7f2,.6,.28), dark=mat(0x172238,.7,.28), blue=mat(0x267bdc,.65,.25), concrete=mat(0x28384c,.1,.9);
    function mesh(geo,material,parent,x=0,y=0,z=0){const m=new T.Mesh(geo,material);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
    function box(w,h,d,material,parent,x=0,y=0,z=0){return mesh(new T.BoxGeometry(w,h,d),material,parent,x,y,z);}
    function cylinder(r,h,material,parent,x=0,y=0,z=0){return mesh(new T.CylinderGeometry(r,r,h,24),material,parent,x,y,z);}
    function beam(a,b,r,material,parent){const start=new T.Vector3(...a),end=new T.Vector3(...b);const m=cylinder(r,start.distanceTo(end),material,parent);m.position.copy(start).add(end).multiplyScalar(.5);m.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),end.sub(start).normalize());return m;}
    box(24,.3,20,concrete,scene,0,-.3,0);
    const grid=new T.GridHelper(24,24,0x4b698b,0x34465f);grid.position.y=-.13;scene.add(grid);
    const rotors=[], movers=[];let drone,arm,scan;
    const factory=host.dataset.scene==='factory';
    if (!factory) {
      for(let i=-10;i<=10;i+=.65)box(2.7,.16,.22,dark,scene,0,0,i);
      [-.85,.85].forEach(x=>box(.13,.2,22,white,scene,x,.16,0));
      for(let z=-8;z<=8;z+=5){beam([-2.5,0,z],[-2.5,4,z],.07,white,scene);beam([2.5,0,z],[2.5,4,z],.07,white,scene);beam([-2.5,4,z],[2.5,4,z],.07,white,scene);}
      drone=new T.Group();scene.add(drone);drone.position.set(0,5.5,0);
      const body=mesh(new T.SphereGeometry(1,32,16),white,drone);body.scale.set(.65,.28,.95);
      box(.7,.2,.85,dark,drone,0,.2,0);box(.18,.06,.7,blue,drone,0,.33,0);
      for(const x of [-1.4,1.4])for(const z of [-1.3,1.3]){
        beam([x*.25,0,z*.25],[x,.04,z],.085,dark,drone);
        cylinder(.16,.24,white,drone,x,.1,z);
        const rotor=new T.Group();rotor.position.set(x,.26,z);drone.add(rotor);
        box(1.35,.025,.11,dark,rotor);box(.11,.025,1.35,dark,rotor);cylinder(.09,.09,blue,rotor);rotors.push(rotor);
        beam([x*.5,-.05,z*.45],[x*.6,-.75,z*.55],.035,white,drone);
      }
      for(const x of [-.85,.85])beam([x,-.75,-.95],[x,-.75,.95],.04,dark,drone);
      cylinder(.18,.25,dark,drone,0,-.38,.65);
      const cam=mesh(new T.SphereGeometry(.24,24,16),dark,drone,0,-.6,.65);
      const lens=cylinder(.13,.12,blue,cam,0,0,.21);lens.rotation.x=Math.PI/2;
      scan=mesh(new T.ConeGeometry(1.7,4.5,32,1,true),new T.MeshBasicMaterial({color:0x4bafff,transparent:true,opacity:.08,depthWrite:false,side:T.DoubleSide}),scene,0,2.5,0);
      const ring=mesh(new T.RingGeometry(1.4,1.48,64),new T.MeshBasicMaterial({color:0x60baff,side:T.DoubleSide}),scene,0,.25,0);ring.rotation.x=-Math.PI/2;movers.push(ring);
    } else {
      box(12,.3,2,dark,scene,0,.8,0);
      for(let x=-5.8;x<6;x+=.4){const roller=cylinder(.15,1.8,white,scene,x,1,0);roller.rotation.x=Math.PI/2;}
      for(const x of [-5,5]){box(2,2.5,2.2,white,scene,x,1.25,-3);box(1.3,.8,.08,dark,scene,x,2,-1.86);box(.8,.08,.1,blue,scene,x,2.1,-1.8);}
      cylinder(.7,.5,dark,scene,0,.2,-2.3);
      arm=new T.Group();arm.position.set(0,.5,-2.3);scene.add(arm);
      beam([0,0,0],[0,2,0],.23,blue,arm);mesh(new T.SphereGeometry(.32,24,16),white,arm,0,2,0);
      beam([0,2,0],[1.4,3.1,0],.2,blue,arm);mesh(new T.SphereGeometry(.28,24,16),white,arm,1.4,3.1,0);
      beam([1.4,3.1,0],[1.7,2.1,1.3],.14,dark,arm);box(.5,.25,.4,white,arm,1.7,2,1.3);
      for(let i=0;i<4;i++)movers.push(box(.65,.5,.65,blue,scene,-5+i*3,1.4,0));
    }
    let angle=.65,elevation=.55,paused=reduced.matches,visible=false,time=0,last=0,frame=0;
    const pause=host.querySelector('[data-stage-pause]'),reset=host.querySelector('[data-stage-reset]');
    function view(){const distance=factory?17:19;camera.position.set(Math.sin(angle)*Math.cos(elevation)*distance,Math.sin(elevation)*distance,Math.cos(angle)*Math.cos(elevation)*distance);camera.lookAt(0,factory?1:2,0);}
    function render(now=0){frame=0;if(!visible||document.hidden)return;const delta=last?Math.min((now-last)/1000,.05):0;last=now;if(!paused)time+=delta;
      if(drone){drone.position.z=Math.sin(time*.32)*2.8;drone.position.y=5.5+Math.sin(time*1.1)*.12;drone.rotation.z=Math.sin(time*.6)*.035;drone.rotation.y=Math.sin(time*.32)*.12;rotors.forEach((r,i)=>r.rotation.y=time*24*(i%2?1:-1));scan.position.z=drone.position.z;movers[0].position.z=drone.position.z;}
      if(arm){arm.rotation.y=Math.sin(time*.7)*.6;movers.forEach((m,i)=>m.position.x=((time*.7+i*3)%12)-6);}
      view();renderer.render(scene,camera);if(!paused)frame=requestAnimationFrame(render);
    }
    function wake(){if(!frame){last=0;frame=requestAnimationFrame(render);}}
    function size(){renderer.setSize(viewport.clientWidth,viewport.clientHeight,false);camera.aspect=viewport.clientWidth/viewport.clientHeight;camera.updateProjectionMatrix();wake();}
    new ResizeObserver(size).observe(viewport);
    new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)wake();else{cancelAnimationFrame(frame);frame=0;}},{threshold:.05}).observe(host);
    document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;}else wake();});
    function label(){pause.textContent=paused?'Play motion':'Pause motion';}
    pause.addEventListener('click',()=>{paused=!paused;label();wake();});reset.addEventListener('click',()=>{angle=.65;elevation=.55;wake();});
    reduced.addEventListener('change',()=>{paused=reduced.matches;label();wake();});
    let pointer=null;
    canvas.tabIndex=0;
    canvas.addEventListener('keydown',e=>{
      if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key))return;
      e.preventDefault();
      if(e.key==='ArrowLeft')angle-=.12;
      if(e.key==='ArrowRight')angle+=.12;
      if(e.key==='ArrowUp')elevation=Math.min(1.2,elevation+.08);
      if(e.key==='ArrowDown')elevation=Math.max(.2,elevation-.08);
      wake();
    });
    canvas.addEventListener('pointerdown',e=>{pointer={id:e.pointerId,x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);});
    canvas.addEventListener('pointermove',e=>{if(!pointer||pointer.id!==e.pointerId)return;angle-=(e.clientX-pointer.x)*.006;elevation=Math.max(.2,Math.min(1.2,elevation+(e.clientY-pointer.y)*.004));pointer.x=e.clientX;pointer.y=e.clientY;wake();});
    ['pointerup','pointercancel'].forEach(type=>canvas.addEventListener(type,()=>pointer=null));
    canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();cancelAnimationFrame(frame);frame=0;canvas.hidden=true;host.querySelector('.stage-fallback').hidden=false;pause.hidden=true;reset.hidden=true;});
    size();label();canvas.hidden=false;host.querySelector('.stage-fallback').hidden=true;pause.hidden=false;reset.hidden=false;
  } catch(error) { console.warn('3D preview unavailable; keeping the simulation image.',error); }
}
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){observer.unobserve(entry.target);mount(entry.target);}}),{rootMargin:'250px'});
document.querySelectorAll('.physical-stage').forEach(host=>observer.observe(host));
