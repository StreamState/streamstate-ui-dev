const k8s = require('@kubernetes/client-node');
const https = require('https')
const kc = new k8s.KubeConfig()
kc.loadFromDefault()
const k8sApi = kc.makeApiClient(k8s.CoreV1Api)
const {createNewSecret}=require('./utils')
//const k8sApiCustomObject = kc.makeApiClient(k8s.CustomObjectsApi)

const fastify = require('fastify')()

const path = require('path')
fastify.register(require('fastify-static'), {
    root: path.join(__dirname, 'public'),
    prefix: '/public/', // optional: default '/'
})
fastify.register(require('fastify-formbody'))
const {
    CONFLUENT_KEY_NAME: confluentKeyName,
    CONFLUENT_SECRET_NAME: confluentSecretName,
    NAMESPACE: namespace,
} = process.env

fastify.post('/confluent/create', (req, reply) => {
    return Promise.all([
        createNewSecret(confluentKeyName, req.body.confluentKey, k8s, k8sApi,namespace, 'key'),
        createNewSecret(confluentSecretName, req.body.confluentSecret, k8s, k8sApi,namespace, 'secret')
    ]).then(_ => reply.send({ success: true }))
        .catch(e => {
            console.log(e)
            reply.send({ error: e.message })
        })
})


fastify.listen(process.env.PORT, '0.0.0.0').then((address) => {
    console.log(`Server running at ${address}`);
})
fastify.get('/', (req, reply) => {
    return reply.sendFile('hello.html') // serving path.join(__dirname, 'public', 'myHtml.html') directly
})

