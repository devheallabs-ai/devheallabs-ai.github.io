const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const script=fs.readFileSync(path.join(__dirname,'../../assets/customer-journey.js'),'utf8');
function setup(valid=true, interest="dummu", offer=""){
 const nodes=new Map();const node=id=>{if(!nodes.has(id))nodes.set(id,{hidden:true,value:'',textContent:'',handlers:{},addEventListener(k,f){this.handlers[k]=f;},scrollIntoView(){},focus(){},select(){}});return nodes.get(id);};
 const form=node('enquiry-form');form.elements={interest:{value:''},request:{value:''}};form.reportValidity=()=>valid;
 const fields={name:'QA',email:'qa@example.com',company:'A & B',interest:'SteadyState platform demonstration',challenge:'తెలుగు + ? & test',availability:''};
 const context={document:{getElementById:node,querySelectorAll:()=>[]},location:{search:'?interest='+interest+'&offer='+offer},URLSearchParams,encodeURIComponent,FormData:class{get(k){return fields[k];}},navigator:{clipboard:{writeText:async()=>{throw new Error('denied');}}}};
 vm.runInNewContext(script,context);return {node,form,fields};
}
test('invalid enquiry cannot create a mail draft',()=>{const x=setup(false);x.form.handlers.submit({preventDefault(){}});assert.equal(x.node('enquiry-result').hidden,true);});
test('enquiry preserves Unicode and reserved characters in email body',()=>{const x=setup();x.form.handlers.submit({preventDefault(){}});const u=new URL(x.node('enquiry-email').href);assert.match(u.searchParams.get('body'),/తెలుగు \+ \? & test/);assert.equal(u.pathname,'sales@devheallabs.com');assert.equal(x.node('enquiry-result').hidden,false);assert.equal(x.form.elements.interest.value,'SteadyState platform demonstration');});
test('clipboard denial leaves a manual-copy route',async()=>{const x=setup();await x.node('copy-enquiry').handlers.click();assert.match(x.node('copy-status').textContent,/Select and copy/);});

for (const [interest,label] of Object.entries({steadystate:"SteadyState platform demonstration",dummu:"SteadyState platform demonstration",nova:"Nova model demonstration",podotl:"Podotl intelligence demonstration"})) { test(`product enquiry selects ${interest}`,()=>{ const x=setup(true,interest); assert.equal(x.form.elements.interest.value,label); const html=fs.readFileSync(path.join(__dirname,"../../contact/index.html"),"utf8"); assert.ok(html.includes(`<option>${label}</option>`)); }); }

test("free pilot query selects request without submitting",()=>{const x=setup(true,"nova","pilot");assert.equal(x.form.elements.request.value,"Free pilot");assert.equal(x.form.elements.interest.value,"Nova model demonstration");assert.equal(x.node("enquiry-result").hidden,true);});

test("partnership CTA selects collaboration enquiry",()=>{const x=setup(true,"partnership","collaboration");assert.equal(x.form.elements.interest.value,"Partnership & collaboration");assert.equal(x.form.elements.request.value,"Partnership discussion");assert.equal(x.node("enquiry-result").hidden,true);});


test('Physical AI pilot preselects the matching form option without submitting',()=>{
 const x=setup(true,'physical-ai','pilot');
 assert.equal(x.form.elements.interest.value,'Physical AI demonstration & pilot');
 assert.equal(x.form.elements.request.value,'Free pilot');
 assert.equal(x.node('enquiry-result').hidden,true);
 const html=fs.readFileSync(path.join(__dirname,'../../contact/index.html'),'utf8');
 assert.ok(html.includes('<option>Physical AI demonstration &amp; pilot</option>'));
});
