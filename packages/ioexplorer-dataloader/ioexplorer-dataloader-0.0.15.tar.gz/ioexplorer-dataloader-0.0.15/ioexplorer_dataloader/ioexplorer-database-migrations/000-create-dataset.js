'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('datasets', {
      id: {
        primaryKey: true,
        autoIncrement: true,
        type: Sequelize.INTEGER,
        allowNull: false
      },
      name: {
        allowNull: false,
        type: Sequelize.STRING,
        validate: {
          notEmpty: true
        },
      },
      description: {
        type: Sequelize.STRING
      },
      cancer_types: {
        type: Sequelize.STRING
      },
      treatment: {
        type: Sequelize.STRING
      },
      available_data: {
        type: Sequelize.STRING
      },
      url: {
        type: Sequelize.STRING,
        validate: {
          isUrl: true
        }
      },
      config: {
        type: Sequelize.JSON
      },
      created_at: {
        allowNull: false,
        defaultValue: new Date(),
        type: Sequelize.DATE
      },
      updated_at: {
        allowNull: false,
        defaultValue: new Date(),
        type: Sequelize.DATE
      },
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('datasets');
  }
};
