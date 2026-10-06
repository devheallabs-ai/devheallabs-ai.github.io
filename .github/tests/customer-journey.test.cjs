const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const script=fs.readFileSync(path.join(__dirname,'../../assets/customer-journey.js'),'utf8');
function setup(valid=true){
 const nodes=new Map();const node=id=>{if(!nodes.has(id))nodes.set(id,{hidden:true,value:'',textContent:'',handlers:{},addEventListener(k,f){this.handlers[k]=f;},scrollIntoView(){},focus(){},select(){}});return nodes.get(id);};
 const form=node('enquiry-form');form.elements={interest:{value:''}};form.reportValidity=()=>valid;
 const fields={name:'QA',email:'qa@example.com',company:'A & B',interest:'Dummu demonstration',challenge:'తెలుగు + ? & test',availability:''};
 const context={document:{getElementById:node,querySelectorAll:()=>[]},location:{search:'?interest=dummu'},URLSearchParams,encodeURIComponent,FormData:class{get(k){return fields[k];}},navigator:{clipboard:{writeText:async()=>{throw new Error('denied');}}}};
 vm.runInNewContext(script,context);return {node,form,fields};
}
test('invalid enquiry cannot create a mail draft',()=>{const x=setup(false);x.form.handlers.submit({preventDefault(){}});assert.equal(x.node('enquiry-result').hidden,true);});
test('enquiry preserves Unicode and reserved characters in email body',()=>{const x=setup();x.form.handlers.submit({preventDefault(){}});const u=new URL(x.node('enquiry-email').href);assert.match(u.searchParams.get('body'),/తెలుగు \+ \? & test/);assert.equal(u.pathname,'sales@devheallabs.com');assert.equal(x.node('enquiry-result').hidden,false);assert.equal(x.form.elements.interest.value,'Dummu demonstration');});
test('clipboard denial leaves a manual-copy route',async()=>{const x=setup();await x.node('copy-enquiry').handlers.click();assert.match(x.node('copy-status').textContent,/Select and copy/);});
