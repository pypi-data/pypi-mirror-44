'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('mutations', {
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
      variant_classification: {
        type: Sequelize.STRING
      },
      hgvcp_short: {
        type: Sequelize.STRING
      },
      entrez_gene_id: {
        type: Sequelize.INTEGER
      },
      protein_position: {
        type: Sequelize.INTEGER
      },
      swissprot: {
        type: Sequelize.STRING
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
      return queryInterface.addIndex('mutations', {
        fields: ['hugo_symbol']
      });
    }).then(() => {
      return queryInterface.addIndex('mutations', {
        fields: ['entrez_gene_id']
      });
    }).then(() => {
      return queryInterface.addIndex('mutations', {
        fields: ['sample_id']
      });
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('mutations');
  }
};