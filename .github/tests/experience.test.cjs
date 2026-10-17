const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../../assets/experience.js'),'utf8');
function setup(missing=false){
 const panels=[{hidden:false},{hidden:false}];
 const buttons=panels.map((_,i)=>({dataset:{panel:String(i)},attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,fn){this.events[k]=fn},focus(){this.focused=true}}));
 const group={querySelectorAll(){return buttons}};
 vm.runInNewContext(source,{document:{querySelectorAll(){return [group]},getElementById(id){return missing?null:panels[Number(id)]}},window:{matchMedia(){return {matches:true}}}});
 return {buttons,panels};
}
test('priority and screenshot selectors switch panels without navigation',()=>{
 const {buttons,panels}=setup();assert.deepEqual(panels.map(p=>p.hidden),[false,true]);
 buttons[1].events.click();assert.deepEqual(panels.map(p=>p.hidden),[true,false]);assert.equal(buttons[1].attrs['aria-pressed'],'true');
});
test('selector keyboard wraps and supports Home and End',()=>{
 const {buttons,panels}=setup();let prevented=false;
 buttons[0].events.keydown({key:'ArrowLeft',preventDefault(){prevented=true}});assert.equal(prevented,true);assert.equal(buttons[1].focused,true);assert.equal(panels[1].hidden,false);
 buttons[1].events.keydown({key:'Home',preventDefault(){}});assert.equal(panels[0].hidden,false);
 buttons[0].events.keydown({key:'End',preventDefault(){}});assert.equal(panels[1].hidden,false);
});
test('incomplete selector leaves content visible',()=>{const {panels}=setup(true);assert.ok(panels.every(p=>!p.hidden));});
