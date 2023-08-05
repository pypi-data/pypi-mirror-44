'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('subjects', {
      id: {
        primaryKey: true,
        autoIncrement: true,
        type: Sequelize.INTEGER,
        allowNull: false
      },
      subject_label: {
        type: Sequelize.STRING
      },
      dataset_id: {
        type: Sequelize.INTEGER,
        references: {
          model: 'datasets',
          key: 'id'
        },
        onDelete: 'cascade'
      },
      age: {
        type: Sequelize.FLOAT
      },
      sex: {
        type: Sequelize.ENUM('MALE', 'FEMALE', 'NA')
      },
      os_months: {
        type: Sequelize.FLOAT,
        validate: {
          min: 0
        }
      },
      os_status: {
        type: Sequelize.ENUM('LIVING', 'DECEASED', 'NA')
      },
      pfs_months: {
        type: Sequelize.FLOAT,
        validate: {
          min: 0
        }
      },
      pfs_status: {
        type: Sequelize.ENUM('PROGRESSED', 'NOPROGRESSION', 'NA')
      },
      m_stage: {
        type: Sequelize.ENUM(
          'M0',
          'M1',
          'MX',
          'M1A',
          'M1B',
          'M1C',
          'NA'
        )
      },
      recist: {
        type: Sequelize.ENUM(
          'PD',
          'SD',
          'PR',
          'CR',
          'NA'
        )
      },
      raw_investigator_response: {
        type: Sequelize.STRING
      },
      ipop_response_2: {
        type: Sequelize.ENUM(
          'NonResponder',
          'Responder',
          'NA'
        )
      },
      ipop_response_3: {
        type: Sequelize.ENUM(
          'NonResponder',
          'Stable',
          'Responder',
          'NA'
        )
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
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('subjects');
  }
};
