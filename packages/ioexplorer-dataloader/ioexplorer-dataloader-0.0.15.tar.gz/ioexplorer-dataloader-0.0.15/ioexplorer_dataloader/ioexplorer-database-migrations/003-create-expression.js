'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('expressions', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      sample_id: {
        type: Sequelize.INTEGER,
        references: {
          model: 'samples',
          key: 'id'
        },
        onDelete: 'cascade'
      },
      hugo_symbol: {
        type: Sequelize.STRING
      },
      entrez_gene_id: {
        type: Sequelize.INTEGER
      },
      raw: {
        type: Sequelize.INTEGER
      },
      fpkm: {
        type: Sequelize.FLOAT
      },
      rld: {
        type: Sequelize.FLOAT
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
      }
    }).then(() => {
      return queryInterface.addIndex('expressions', {
        fields: ['sample_id']
      })
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('expressions');
  }
};