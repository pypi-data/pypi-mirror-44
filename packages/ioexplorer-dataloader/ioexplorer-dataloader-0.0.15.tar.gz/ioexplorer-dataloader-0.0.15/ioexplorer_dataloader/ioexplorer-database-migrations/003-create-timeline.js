'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('timelines', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      subject_id: {
        type: Sequelize.INTEGER,
        references: {
          model: 'subjects',
          key: 'id'
        },
        onDelete: 'cascade'
      },
      start_date: {
        type: Sequelize.INTEGER
      },
      stop_date: {
        type: Sequelize.INTEGER
      },
      event_type: {
        type: Sequelize.STRING
      },
      treatment_type: {
        type: Sequelize.STRING
      },
      subtype: {
        type: Sequelize.STRING
      },
      agent: {
        type: Sequelize.STRING
      },
      chemo_cycles: {
        type: Sequelize.STRING
      },
      comments: {
        type: Sequelize.STRING
      },
      treatment_best_response: {
        type: Sequelize.STRING
      },
      overall_response: {
        type: Sequelize.STRING
      },
      reason_for_tx_discontinuation: {
        type: Sequelize.STRING
      },
      note: {
        type: Sequelize.STRING
      },
      surgery_details: {
        type: Sequelize.STRING
      },
      source_string: {
        type: Sequelize.STRING
      },
      status_string: {
        type: Sequelize.STRING
      },
      specimen_type: {
        type: Sequelize.STRING
      },
      treatment_details: {
        type: Sequelize.STRING
      },
      source_lab: {
        type: Sequelize.STRING
      },
      surgery: {
        type: Sequelize.STRING
      },
      event_details: {
        type: Sequelize.STRING
      },
      dosage: {
        type: Sequelize.STRING
      },
      karnofsky_performance: {
        type: Sequelize.STRING
      },
      specimen_site: {
        type: Sequelize.STRING
      },
      type_of_surgery: {
        type: Sequelize.STRING
      },
      disgnostic_type: {
        type: Sequelize.STRING
      },
      disgnostic_type_detailed: {
        type: Sequelize.STRING
      },
      concurrent_chemo: {
        type: Sequelize.STRING
      },
      mgmt_status: {
        type: Sequelize.STRING
      },
      event_type_detailed: {
        type: Sequelize.STRING
      },
      histology: {
        type: Sequelize.STRING
      },
      who_grade: {
        type: Sequelize.STRING
      },
      source_pathology: {
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
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('timelines');
  }
};