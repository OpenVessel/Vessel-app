

/// --------- lib.js ---------

// Set before importing `ohif-viewer` (JS Object)


// ------- Main.js  In the application
import UINotificationService from '@ohif/core';
const servicesManager = new ServicesManager();

servicesManager.registerService(UINotificationService);

// UI Service Provider
useEffect(() => {
  if (service) {
    service.setServiceImplementation({ hide, show });
  }
}, [service, hide, show]);

// In an extension
const { UINotificationService } = servicesManager.services;

if (UINotificationService) {
  UINotificationService.show('Hello from the other side 👋');
}


window.config = {
  // default: '/'
  routerBasename: '/',
  servers: {
    dicomWeb: [
      {
        name: 'DCM4CHEE',
        wadoUriRoot: 'https://server.dcmjs.org/dcm4chee-arc/aets/DCM4CHEE/wado',
        qidoRoot: 'https://server.dcmjs.org/dcm4chee-arc/aets/DCM4CHEE/rs',
        wadoRoot: 'https://server.dcmjs.org/dcm4chee-arc/aets/DCM4CHEE/rs',
        qidoSupportsIncludeField: true,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
      },
    ],
  },
};